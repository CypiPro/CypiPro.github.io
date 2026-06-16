import hickle as hkl
import numpy as np
import nnet as net
import matplotlib.pyplot as plt
size1 = 20
size2 = 20

x1 = np.outer(np.linspace(-2, 2, size1), np.ones(size1))
x2 = np.outer(np.linspace(-2, 2, size2), np.ones(size2)).T

x = np.vstack([x1.ravel(), x2.ravel()])
# y_t_n = np.cos(np.pi*x1*x2)
y_t_n = np.pow(np.abs(x1)+0.1, x2)

y_t = y_t_n.ravel().reshape(1, -1)
max_epoch = 50000
err_goal = 0.1
disp_freq = 1000
lr = 0.0013
mc = 0.9

L = x.shape[0]
K1 = 15
K2 = 10
K3 = y_t.shape[0]

ksi_inc = 1.05
ksi_dec = 0.8
er = 1.04

SSE_vec = []

w1, b1 = net.nwtan(K1, L)
w2, b2 = net.nwtan(K2, K1)
w3, b3 = net.rands(K3, K2)

hkl.dump([w1,b1,w2,b2], 'wagi2w.hkl')
w1,b1,w2,b2 = hkl.load('wagi2w.hkl')

plt.ion()
fig = plt.figure(figsize=(18, 5))
w1_t_1, b1_t_1, w2_t_1, b2_t_1, w3_t_1, b3_t_1 = w1, b1, w2, b2, w3, b3

SSE = 0
lr_vec = list()

for epoch in range(1, max_epoch+1):
    y1 = net.tansig(np.dot(w1, x), b1)
    y2 = net.tansig(np.dot(w2, y1), b2)
    y3 = net.purelin(np.dot(w3, y2), b3)

    e = y_t - y3

    SSE_t_1 = SSE
    SSE = net.sumsqr(e)
    if np.isnan(SSE):
        break
    else:
        if SSE > er * SSE_t_1:
            lr *= ksi_dec
        elif SSE < SSE_t_1:
            lr *= ksi_inc
    lr_vec.append(lr)

    d3 = net.deltalin(y3, e)
    d2 = net.deltatan(y2, d3, w3)
    d1 = net.deltatan(y1, d2, w2)

    dw1, db1 = net.learnbp(x, d1, lr)
    dw2, db2 = net.learnbp(y1, d2, lr)
    dw3, db3 = net.learnbp(y2, d3, lr)

    w1_temp, b1_temp, w2_temp, b2_temp, w3_temp, b3_temp = \
    w1.copy(), b1.copy(), w2.copy(), b2.copy(), w3.copy(), b3.copy()

    w1 += dw1 + mc * (w1 - w1_t_1)
    b1 += db1 + mc * (b1 - b1_t_1)

    w2 += dw2 + mc * (w2 - w2_t_1)
    b2 += db2 + mc * (b2 - b2_t_1)

    w3 += dw3 + mc * (w3 - w3_t_1)
    b3 += db3 + mc * (b3 - b3_t_1)

    w1_t_1, b1_t_1, w2_t_1, b2_t_1, w3_t_1, b3_t_1 = \
    w1_temp, b1_temp, w2_temp, b2_temp, w3_temp, b3_temp

    SSE = net.sumsqr(e)
    if np.isnan(SSE):
        break
    SSE_vec.append(SSE)
    if SSE < err_goal:
        break
    if (epoch % disp_freq) == 0:
        print("Epoch: %5d | SSE: %0.5f " % (epoch, SSE))
        y3_grid = y3.reshape(size1, size2)
        err_grid = y_t_n - y3_grid
        plt.clf()

        # -------------------------
        # 1. Prawdziwa funkcja y_t
        # -------------------------
        ax1 = fig.add_subplot(1, 3, 1, projection='3d')
        ax1.plot_surface(x1, x2, y_t_n, cmap='viridis', edgecolor='none', alpha=0.9)
        ax1.set_title('Prawdziwa funkcja y_t')
        ax1.set_xlabel('x1')
        ax1.set_ylabel('x2')
        ax1.set_zlabel('y_t')

        # -------------------------
        # 2. Wynik sieci y3
        # -------------------------
        ax2 = fig.add_subplot(1, 3, 2, projection='3d')
        ax2.plot_surface(x1, x2, y3_grid, cmap='plasma', edgecolor='none', alpha=0.9)
        ax2.set_title('Wynik sieci y3')
        ax2.set_xlabel('x1')
        ax2.set_ylabel('x2')
        ax2.set_zlabel('y3')

        # -------------------------
        # 3. Powierzchnia błędu
        # -------------------------
        ax3 = fig.add_subplot(1, 3, 3, projection='3d')
        ax3.plot_surface(x1, x2, err_grid, cmap='coolwarm', edgecolor='none')
        ax3.set_title('e')
        ax3.set_xlabel('x1')
        ax3.set_ylabel('x2')
        ax3.set_zlabel('error')

        plt.tight_layout()
        plt.draw()
        plt.pause(1e-3)
plt.ioff()
print("Epoch: %5d | SSE: %0.5f " % (epoch, SSE))
plt.figure()
plt.plot(SSE_vec)
plt.ylabel('SSE')
plt.yscale('linear')
plt.title('epoch')
plt.grid(True)
plt.draw()
plt.show()
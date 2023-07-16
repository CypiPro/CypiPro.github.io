// background scrolling

window.addEventListener("scroll", function () {
    var scrollTop = document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;

    var scrolledPercentage = scrollTop / (scrollHeight - clientHeight);

    document.body.style.backgroundPosition = `center ${scrolledPercentage*60}%`;
});
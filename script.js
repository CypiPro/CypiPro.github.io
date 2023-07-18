// background scrolling

window.addEventListener("scroll", function () {
    var scrollTop = document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;

    var scrolledPercentage = scrollTop / (scrollHeight - clientHeight);

    document.body.style.backgroundPosition = `center ${scrolledPercentage*60}%`;
});


// custom scroll bar

    // scrolling
const scrollBar = document.getElementById("scrollbar");
const scrollThumb = document.getElementById("scrollbarThumb");

window.addEventListener("scroll", function () {
    var scrollTop = document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;

    var scrollbarHeight = scrollBar.offsetHeight;
    var thumbHeight = scrollThumb.offsetHeight;

    var scrolledPercentage = scrollTop / (scrollHeight - clientHeight);

    scrollThumb.style.top = `${scrolledPercentage *(scrollbarHeight -thumbHeight)}px`;
});

let isDragging = false;
let lastY = 0;

scrollThumb.addEventListener("mousedown", function (e) {
    isDragging = true;
    lastY = e.clientY;
});

window.addEventListener("mousemove", function (e) {
    if (isDragging) {
        var scrollHeight = document.documentElement.scrollHeight;
        var clientHeight = document.documentElement.clientHeight;

        var scrollbarHeight = scrollBar.offsetHeight;
        var thumbHeight = scrollThumb.offsetHeight;

        var deltaY = e.clientY - lastY;
        var thumbTop = parseInt(scrollThumb.style.top) || 0;
        var newThumbTop = thumbTop + deltaY;

        if (newThumbTop < 0) {
            newThumbTop = 0;
        } else if (newThumbTop > scrollbarHeight - thumbHeight) {
            newThumbTop = scrollbarHeight - thumbHeight;
        }

        var scrolledPercentage = newThumbTop / (scrollbarHeight - thumbHeight);
        var newScrollTop = scrolledPercentage * (scrollHeight - clientHeight);

        document.documentElement.scrollTop = newScrollTop;
        scrollThumb.style.top = `${newThumbTop}px`;

        lastY = e.clientY;
    }
});

window.addEventListener("mouseup", function () {
    isDragging = false;
});


    // table of contents
let headers = document.getElementsByTagName("h1");
var scrollHeight = document.documentElement.scrollHeight;
var scrollbarHeight = scrollBar.offsetHeight;

for (let i = 0; i < headers.length; i++) {
    let header = headers[i];

    var offsetTop = header.offsetTop;

    var label = document.createElement("label");
    label.onclick = function () {header.parentElement.scrollIntoView({behavior:"smooth"})};

    scrollBar.appendChild(label);
    label.style.top = `${(offsetTop/scrollHeight)*scrollbarHeight}px`;

    label.innerText = header.innerText;
};
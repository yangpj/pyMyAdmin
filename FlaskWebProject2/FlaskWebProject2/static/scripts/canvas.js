/* declare global variables here */
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

var sprite = createImageSprite("/static/content/res/zs_001041_Attack_02_0005.png");


canvas.addEventListener('mousedown', OnMouseDown);
canvas.addEventListener('mousemove', OnMouseMove);
//canvas.addEventListener('mousedown', OnMouseDown);

function OnMouseDown(e) {
    console.log(e);
}

function OnMouseMove(e) {
    //e.preventDefault();
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    drawBackground("Hello Canvas");
    var o = document.getElementById("mouse-pos");
    var pos = windowToCanvas(e.clientX, e.clientY);
    o.innerText = "x: " + pos.x + ", " + "y: " + pos.y;
    drawSprite();
    
    //console.log(e);
}

function windowToCanvas(x, y) {
    var bbox = canvas.getBoundingClientRect();
    // 包围盒的大小不一定等于画布大小，所以需要缩放
    return {x : x - bbox.left * (canvas.width / bbox.width),
            y : y - bbox.top * (canvas.height / bbox.height)};
}

function createImageSprite(url) {
    var sp = new Image();
    sp.src = url;
    sp.onload = drawSprite;
    return sp;
}

function drawSprite() {
    context.drawImage(sprite, 0 + 0.5, 0 + 0.5);
}

/* NOTE: This code don't work with IE */
function downloadCanvas(theLink) {
    theLink.href = document.getElementById("canvas").toDataURL();
    theLink.download = 'canvas.png';
    return true;
}

function drawCircle(x, y, redius, fill) {
    var needFill = fill || false;
    context.beginPath();
    context.arc(x, y, redius, 0, Math.PI * 2, true);
    context.stroke();
    if (needFill) {
        context.fill();
    }
}

function drawBackground(text) {

    // 圆形
    drawCircle(130, 130, 100, true);

    // 文本
    context.font = "40pt 微软雅黑";
    context.fillText(text, 400, 300);
}

function initContext() {
    context.fillStyle = 'red'
    context.strokeStyle = 'white';
    // shadow
    context.shadowColor = '#200772';
    context.shadowOffsetX = 2;
    context.shadowOffsetY = 6;
    context.shadowBlur = 10;
}

initContext();
drawBackground("Hello Canvas");

/*
 *----------------------------------------------------------------------
 *
 * ShowCurrentDate --
 *
 *	Show current timestamp and flush once per second.
 *
 * Results:
 *	None.
 *
 * Side effects:
 *	Appends a new text node to <div> if not exists.
 *
 *----------------------------------------------------------------------
 */
function ShowCurrentDate() {
    var me = this;
    this.waitAndCall = function () {
        window.setTimeout(function () {
            var timeBox = document.getElementById("timeBox");
            if (timeBox) {
                if (!timeBox.firstChild) {
                    var node = document.createTextNode(Date());
                    timeBox.appendChild(node);
                }
                else {
                    timeBox.firstChild.nodeValue = Date();
                }
            }
            else {
                return;
            }
            me.waitAndCall();
        }, 1000);
    }
}

//new ShowCurrentDate().waitAndCall();

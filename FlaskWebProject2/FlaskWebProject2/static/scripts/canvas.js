/* declare global variables here */
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

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

function drawText(text) {

    console.log("画布宽度：" + context.canvas.width);
    console.log("画布高度：" + context.canvas.height);

    // assign gradients to fill
    context.fillStyle = 'red'
    context.strokeStyle = 'white';

    //context.clearRect(0, 0, context.canvas.width, context.canvas.height);

    // 渐变效果
    //var lingrad = context.createLinearGradient(0, 1, 0.3, 0.3);
    //lingrad.addColorStop(0, '#500772');
    //lingrad.addColorStop(1, '#20f7ff');

    // Rotation
    //context.rotate(5 * Math.PI / 180);

    drawCircle(120, 120, 100, true);

    //context.save();
    //context.fillStyle = 'green';
    //context.fillRect(0, 0, context.canvas.width, context.canvas.height);
    //context.restore();
    // draw shapes
    //context.fillRect(100, 150, 130, 130);

    // shadow
    context.shadowColor = '#200772';
    context.shadowOffsetX = 2;
    context.shadowOffsetY = 6;
    context.shadowBlur = 10;

    // 文本
    context.font = "40pt 微软雅黑";
    context.fillText(text, 400, 300);

    //context.shadowColor = '#ff00ff';
    //context.shadowOffsetX = 6;
    //context.shadowOffsetY = 2;
    //context.shadowBlur = 4;
    //context.rotate(-10 * Math.PI / 180);
    //context.strokeText(text, 50, 150);
}

drawText("Hello Canvas");

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

var p1;
var p2;

function setup() {
    createCanvas(760, 760);
    p1 = {'x': 10, 'y': 10}
    p2 = {'x': 700, 'y': 700}
}

function draw() {
    background(33);
    stroke(0,255,0);
    strokeWeight(5);
    line(p1.x, p1.y, p2.x, p2.y);
    drawGrid();
}

function drawGrid() {
    stroke(100);
    strokeWeight(1);
    numLines = floor(width / 10);
    for (i = 0; i < numLines; i++) {
        line(10*i, 0, 10*i, height);
        line(0, 10*i, width, 10*i);
    }
}

function drawEndpoints(p1, p2) {
    return 1;
}



function mouseClicked() {
    [p1.x, p1.y] = [p2.x, p2.y];
    [p2.x, p2.y] = [mouseX, mouseY];
}
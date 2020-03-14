var p1;
var p2;

function setup() {
    createCanvas(760, 760);
    p1 = {'x': 10, 'y': 10}
    p2 = {'x': 700, 'y': 700}
}

function draw() {
    background(33);
    drawGrid();
    drawPoint(p1);
    drawPoint(p2);
    stroke(0,255,0);
    line(flrDn(p1.x, 10)+5, flrDn(p1.y, 10)+5, flrDn(p2.x, 10)+5, flrDn(p2.y, 10)+5);
    bresenham(p1, p2);
}

function drawGrid() {
    stroke(63);
    numLines = floor(width / 10);
    for (i = 0; i < numLines; i++) {
        line(10*i, 0, 10*i, height);
        line(0, 10*i, width, 10*i);
    }
}


function drawPoint(p) {
    fill(0,255,0)
    rect(flrDn(p.x, 10), flrDn(p.y, 10), 10, 10);
}


function flrDn(n, r) {
    return floor(n/r) * r
}


function bresenham(p1, p2) {
    return 1
}



function mouseClicked() {
    [p1.x, p1.y] = [p2.x, p2.y];
    [p2.x, p2.y] = [mouseX, mouseY];
}
'use strict';

function Joystick(id, resetOnLeave) {
    this.element = document.getElementById(id);

    if (!this.element) {
        throw "Joystick, object not found by id"
    }

    var pointer = document.createElement('div');
    pointer.className = 'joystick-pointer';
    this.element.appendChild(pointer);

    var elementWidth = this.element.offsetWidth;
    var elementHeight = this.element.offsetHeight;

    var pointerOffsetX = elementWidth - pointer.offsetWidth;
    var pointerOffsetY = elementHeight - pointer.offsetHeight;

    var callback = null;
    var reset = resetOnLeave;

    var currentX = 0;
    var currentY = 0;
    var toggled = false;

    movePointer();

    document.body.addEventListener('touchmove', function(event) {
      event.preventDefault();
    }, false);

    this.element.addEventListener('touchstart', function(e){
        toggled = true;
        runCallback();
    }, false)

    this.element.addEventListener('touchend', function(e){
        toggled = false;

        if (reset) {
            currentX = 0;
            currentY = 0;
            movePointer();
        }

        runCallback();
    }, false)

    this.element.addEventListener('touchmove', function(e){
        var touchObject = e.targetTouches[0];
        currentX = calculateX(this, touchObject);
        currentY = calculateY(this, touchObject);

        movePointer();
        runCallback();
    }, false)

    this.setCallback = function(func) {
        callback = func;
    }

    function movePointer() {
        pointer.style.left = (pointerOffsetX) * ((currentX + 50) / 100) + "px";
        pointer.style.top = (pointerOffsetY) * ((50 - currentY) / 100) + "px";
    }

    function runCallback(){
        if (callback) {
            callback(currentX * 2, currentY * 2, toggled);
        }
    }

    function calculateX(object, touchObject){
        var result = touchObject.pageX - object.offsetLeft;

        if (result < 0)
            result = 0;

        if (result > elementWidth)
            result = elementWidth;

        return Math.round(100 * result / elementWidth)  - 50;
    }

    function calculateY(object, touchObject){
        var result = elementHeight - Math.round(touchObject.pageY - object.offsetTop)

        if (result < 0)
            result = 0;

        if (result > elementHeight)
            result = elementHeight;

        return Math.round(100 * result / elementHeight) - 50;
    }
}
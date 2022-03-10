function addText(text){
    var div = document.getElementById("Time")
    div.innerHTML = text
}
eel.expose(addText)

function StopWatch(){
    eel.StopWatch()
}

function haltWatch(){
    eel.stop()
}
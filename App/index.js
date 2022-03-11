// Shows the stop watch time on the app
function showTime(time){
    var div = document.getElementById("time")
    div.innerHTML = time
}
eel.expose(showTime)

// Starts the stop watch
function StopWatch(){
    eel.StopWatch()
}

// Stops the watch
function haltWatch(){
    eel.stop()
}

// Once form is submitted it is hidden
function hideForm(event){
    event.preventDefault()
    var div = document.getElementById("info")
    div.classList.toggle("hidden")
}

// Once the form is submitted the watch is visible
function showWatch(event){
    event.preventDefault()  
    var div = document.getElementById("watch")
    div.classList.toggle("watch")
}

// Exports input values to Python
function export_input_values(event){
    event.preventDefault()
    var name = document.getElementById("name")
    var description = document.getElementById("description")
    eel.get_form_input([name.value, description.value])
}
eel.expose(export_input_values)

window.onload = () => {
    var submit = document.getElementById("info")
    submit.addEventListener("submit", hideForm, false)
    submit.addEventListener("submit", showWatch, false)
    submit.addEventListener("submit", export_input_values, false)
}

function verifica_ligado() {
    var cb_servo = document.getElementById("servo")
    var cb_rele = document.getElementById("rele")

    if (cb_servo.value == "livre"){
        return
    }

    if (cb_servo.value == "on" && cb_rele.value == "on") {
        cb_servo.checked = true
        cb_rele.checked = true
    }

    else if (cb_servo.value == "off" && cb_rele.value == "off"){
        cb_servo.checked = false
        cb_rele.checked = false
    }

}

window.onload = verifica_ligado();

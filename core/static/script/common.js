$("#usernameId").on("input",()=>{
    const largoTexto = $("#usernameId").val().length;
    const parrafo = $("#pUsernameid");
    const inputUsername = $("#usernameId");

    if (largoTexto <= 2 || largoTexto >= 15 ){
        inputUsername.removeClass("is-valid").addClass("is-invalid");
        parrafo.text("El nombre de usuario debe contener entre 3 y 15 caracteres")
               .css({ color: "red", fontSize: "14px" });
    }else{
        inputUsername.removeClass("is-invalid").addClass("is-valid");
        parrafo.text("").css({ color: "", fontSize: "" });
    }
});

$("#nameId").on("input",()=>{
    const largoTexto = $("#nameId").val().length;
    const parrafo = $("#pNameid");
    const inputName = $("#nameId");

    if (largoTexto <= 3 || largoTexto >= 15 ){
        inputName.removeClass("is-valid").addClass("is-invalid");
        parrafo.text("El nombre de usuario debe contener entre 3 y 15 caracteres")
               .css({ color: "red", fontSize: "14px" });
    }else{
        inputName.removeClass("is-invalid").addClass("is-valid");
        parrafo.text("").css({ color: "", fontSize: "" });
    }
})

$("#lastNameId").on("input",()=>{
    const largoTexto = $("#lastNameId").val().length;
    const parrafo = $("#pLastnameid");
    const inputLastname = $("#lastNameId");

    if (largoTexto <= 3 || largoTexto >= 15 ){
        inputLastname.removeClass("is-valid").addClass("is-invalid");
        parrafo.text("El nombre de usuario debe contener entre 3 y 15 caracteres")
               .css({ color: "red", fontSize: "14px" });
    }else{
        inputLastname.removeClass("is-invalid").addClass("is-valid");
        parrafo.text("").css({ color: "", fontSize: "" });
    }
})

$("#emailId2").on("input", () => {
    const email1 = $("#emailId").val();
    const email2 = $("#emailId2").val();
    const parrafo = $("#pEmailid");

    if (email1 !== email2) {
        $("#emailId, #emailId2").addClass("is-invalid");
        $("#emailId, #emailId2").removeClass("is-valid");
        parrafo.text("Los correos no coinciden");
        parrafo.css({ color: "red", fontSize: "14px" });
    } else {
        $("#emailId, #emailId2").removeClass("is-invalid");
        $("#emailId, #emailId2").addClass("is-valid");
        parrafo.text("");
    }
});

$("#passwordId2").on("input", () => {
    const pass1 = $("#passwordId").val();
    const pass2 = $("#passwordId2").val();
    const parrafo = $("#pPasswordid");

    if (pass1 !== pass2) {
        $("#passwordId, #passwordId2").addClass("is-invalid");
        $("#passwordId, #passwordId2").removeClass("is-valid");
        parrafo.text("Las contraseñas no coinciden");
        parrafo.css({ color: "red", fontSize: "14px" });
    } else {
        $("#passwordId, #passwordId2").removeClass("is-invalid");
        $("#passwordId, #passwordId2").addClass("is-valid");
        parrafo.text("");
    }
});

function assignRowNumbers() {
    var rows = document.querySelectorAll('.n_fila');
    rows.forEach(function(row, index) {
      var numberCell = row.querySelector('.fila-number');
      numberCell.textContent = index + 1;
    });
  }

  // Llamada a la función para asignar los números de fila inicialmente
  assignRowNumbers();
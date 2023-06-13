// usernameId
// nameId
// lastNameId
// emailId
// emailId2
// passwordId
// passwordId2

$("#usernameId").keyup(()=>{
    const largoTexto = $("#usernameId").length;
    const parrafo = $("#pUsernameid");

    if (largoTexto <= 2 || largoTexto >= 15 ){
        $("#usernameId").addClass("is-invalid");
        $("#usernameId").removeClass("is-valid");
        parrafo.text("El nombre de usuario  debe contener entre 3 a 15 caracteres");
        parrafo.css({ color: "red", fontSize: "14px" });
    }else{
        $("#nombreId").removeClass("is-invalid");
        $("#nombreId").addClass("is-valid");
        parrafo.text("");
    }
})

$("#nameId").keyup(()=>{
    const largoTexto = $("#nameId").length;
    const parrafo = $("#nameId");

    if (largoTexto <= 3 || largoTexto >= 15 ){
        $("#nameId").addClass("is-invalid");
        $("#nameId").removeClass("is-valid");
        parrafo.text("El nombre debe contener entre 3 a 15 caracteres");
        parrafo.css({ color: "red", fontSize: "14px" });
    }else{
        $("#nameId").removeClass("is-invalid");
        $("#nameId").addClass("is-valid");
        parrafo.text("");
    }
})

$("#lastNameId").keyup(()=>{
    const largoTexto = $("#lastNameId").length;
    const parrafo = $("#lastNameId");

    if (largoTexto <= 3 || largoTexto >= 15 ){
        $("#lastNameId").addClass("is-invalid");
        $("#lastNameId").removeClass("is-valid");
        parrafo.text("El apellido debe contener entre 5 a 15 caracteres");
        parrafo.css({ color: "red", fontSize: "14px" });
    }else{
        $("#lastNameId").removeClass("is-invalid");
        $("#lastNameId").addClass("is-valid");
        parrafo.text("");
    }
})

$("#emailId2").keyup(()=>{
    const email1 = $("#emailId").val();
    const email2 = $("emailId2").val();
    const parrafo = $("#pEmailid");
    if (email1 && email2 && email1 != email2){
        $("#emailId").addClass("is-invalid");
        $("#emailId").removeClass("is-valid");
        $("#emailId2").addClass("is-invalid");
        $("#emailId2").removeClass("is-valid");
        parrafo.text("El apellido debe contener entre 5 a 15 caracteres");
        parrafo.css({ color: "red", fontSize: "14px" });
    }else{
        $("#emailId").removeClass("is-invalid");
        $("#emailId").addClass("is-valid");
        $("#emailId2").removeClass("is-invalid");
        $("#emailId2").addClass("is-valid");
        parrafo.text("");
    }
})1

$("#passwordId2").keyup(()=>{
    const email1 = $("#passwordId").val();
    const email2 = $("passwordId2").val();
    const parrafo = $("#pPasswordid");
    if (email1 && email2 && email1 != email2){
        $("#passwordId").addClass("is-invalid");
        $("#passwordId").removeClass("is-valid");
        $("#passwordId2").addClass("is-invalid");
        $("#passwordId2").removeClass("is-valid");
        parrafo.text("El apellido debe contener entre 5 a 15 caracteres");
        parrafo.css({ color: "red", fontSize: "14px" });
    }else{
        $("#passwordId").removeClass("is-invalid");
        $("#passwordId").addClass("is-valid");
        $("#passwordId2").removeClass("is-invalid");
        $("#passwordId2").addClass("is-valid");
        parrafo.text("");
    }
})
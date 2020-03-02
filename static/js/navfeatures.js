for(var x=0; x<5; x++){
    let current_element = x.toString();
    document.getElementById(current_element).addEventListener("mouseenter", function(){
        document.getElementById(current_element).classList.add("select");
    }, false);
    document.getElementById(current_element).addEventListener("mouseleave", function(){
        document.getElementById(current_element).classList.remove("select");
    }, false);
}

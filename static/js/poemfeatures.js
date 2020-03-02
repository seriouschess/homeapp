
var current_id = "5";
document.getElementById(current_id).addEventListener("mouseenter", function(){
    document.getElementById(current_id).classList.add("selectsub");
}, false);
document.getElementById(current_id).addEventListener("mouseleave", function(){
    document.getElementById(current_id).classList.remove("selectsub");
}, false);

var delete_id = "6";
document.getElementById(delete_id).addEventListener("mouseenter", function(){
    document.getElementById(delete_id).classList.add("selectdelete");
}, false);
document.getElementById(delete_id).addEventListener("mouseleave", function(){
    document.getElementById(delete_id).classList.remove("selectdelete");
}, false);


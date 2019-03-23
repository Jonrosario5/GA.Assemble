$(document).ready(function() {
    console.log('jQuery connected')

    $(".navbar-burger").click(function() {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
    
    $(`div .add-event`).click(function(){
        console.log($(this).children('.modal'))
        $(this).children('.modal').toggleClass('is-active')
    });
});
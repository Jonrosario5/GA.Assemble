$(document).ready(function() {
    console.log('jQuery connected')

    $(".navbar-burger").click(function() {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
    
    $('.toggle-user-modal').click(function(){
        $('.edit-user-modal').toggleClass('is-active')
    });
});
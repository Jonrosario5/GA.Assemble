$(document).ready(function() {
    console.log('jQuery connected')

    let selected_topic = '';

    function updateTopic(newTopic) {
        selected_topic = newTopic;
    }
    
    $(".navbar-burger").click(function() {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });

    $('div[data-id]')

    // $('div .topic').click(function(){
    //     console.log($(this).attr('data-name'));
    //     updateTopic($(this).attr('data-name'));
    //     $('.event-header').text(`Upcoming ${selected_topic} Events`);
    //     let data = {"selected_topic": selected_topic}
    //     $.post('/main', JSON.stringify(data));
    // });
    
    $(`div .event`).click(function(){
        console.log($(this).children('.modal'))
        $(this).children('.modal').toggleClass('is-active')
    });
});
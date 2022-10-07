
$(document).ready(function () {

    $('.menu a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location == link) {
            $(this).parent().addClass('active');
        }
    });


    var filterFns = {
        numberGreaterThan50: function () {
            var number = $(this).find('.number').text();
            return parseInt(number, 10) > 50;
        },
        ium: function () {
            var name = $(this).find('.name').text();
            return name.match(/ium$/);
        }
    };
    $('.filters-button-group').on('click', 'button', function (e) {
        e.preventDefault();
        // var filterValue = $(this).attr('data-filter');
        // var sidebar_posts = $(this).attr('data-name');
        var recent = $(this).data('recentjquery');
        var popular = $(this).data('popularjquery');
        // var users = $(this).data('usersjquery');
        do_something(recent, popular, );
        // filterValue = filterFns[filterValue] || filterValue;
        // $grid.isotope({
        //     filter: filterValue
        // });
    });
    // $('.button-group').each(function (i, buttonGroup) {
    //
    //     var $buttonGroup = $(buttonGroup);
    //     $buttonGroup.on('click', 'button', function () {
    //
    //         $buttonGroup.find('.is-checked').removeClass('is-checked');
    //         $(this).addClass('is-checked');
    //     });
    // });
});

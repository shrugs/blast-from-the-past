$(function() {

  var displayFormat = function(friend) {
    var imgURL = "https://graph.facebook.com/" + friend.id + "/picture?type=small";
    return '<span class="item"><img src="' + imgURL + '"></img><span class="friend-name">' + friend.text + '</span></span>';
  };

  $.ajax({
    method: 'GET',
    url: '/friends',
    dataType: 'JSON'
  })
  .success(function(data) {

    $('.loading').fadeOut();
    $('.friends-select').fadeIn().select2({
      data: data.data.map(function(friend){
        return {
          id: friend.id,
          text: friend.name,
        };
      }),
      matcher: function (params, data) {
        // If there are no search terms, return all of the data
        if ($.trim(params.term) === '') {
          return data;
        }

        // `params.term` should be the term that is used for searching
        // `data.text` is the text that is displayed for the data object
        if (data.text.toLowerCase().indexOf(params.term.toLowerCase()) > -1) {
          return data;
        }

        // Return `null` if the term should not be displayed
        return null;
      },
      escapeMarkup: function (markup) { return markup; },
      templateResult: displayFormat,
      templateSelection: displayFormat,
    }).on('select2:select', function() {
      $('.btn-row').show();
    });

  })
  .error(function() {
    console.log('FUCK');
  });


  $('.fuckem-btn').on('click', function() {
    var friendToFuck = $('.friends-select').val();
    $('.request-loading').show();
    $.ajax({
      method: 'GET',
      url: '/fuckem/' + friendToFuck,
    })
    .success(function(data) {
      $('.request-loading').hide();
      if (data === 'no') {
        $('#link').append("<div>Fuck off lol</div>");
      } else {
        var splitted = data.split('_');
        var uid = splitted[0];
        var pid = splitted[1];
        var postURL = 'http://www.facebook.com/' + uid + '/posts/' + pid;
        $('#link').append("<div>Congrats, <a href='" + postURL + "' target='_blank'>this post</a> is now at the top of their friend's feeds.</div>");
      }
    })
    .error(function() {
      console.log('FUCK');
    });

  });

});
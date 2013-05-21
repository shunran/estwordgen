$(function() {
	$('input[type=button]').click(function(event) {
		event.preventDefault();
		$('.content').text('Laadib...');
    	$.post('main.py', 'how='+ $('input[name=how]:checked').val(),
    			function(data) {
            dataLoaded(self, data);
          });
		console.log(this);
	});
	function dataLoaded(marker, data) {
		var answer = $.parseJSON(data);
		var contentElem = $('.content');
		contentElem.html('');
		$.each(answer, function(key, word) {
			var conteiner = $('<div>').addClass('word');
			conteiner.text(word)
			contentElem.append(conteiner);
			console.log(word);
		})
	}
});
$(document).ready(function() {
	// JQuery code to be added in here.
	(function(){
		var userid_in = '';
		if ($('#favorite_userid').length > 0){
			userid_in = $('#favorite_userid').val()
		}
		if ('' == userid_in){
			return;
		}
		$.get('/book/favorite/',{user_id:userid_in}, function(data){
			//console.log(data)
			json_obj = JSON.parse(data);
			var html_val = "";
			for (i=0; i<json_obj.length; i++){
				html_val = html_val + "<div class=\"col-sm-6 col-md-4 col-lg-3\" style=\"font-size: 14px\">";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\">";
                html_val = html_val + "<div style=\"width:150px;height:200px;background: url('/media/" +
					json_obj[i].picture + "') no-repeat center; background-size: contain;\"  alt=\"Picture\" ></div>";
                html_val = html_val + "</a><br>";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\"><strong>" + json_obj[i].name + "</strong></a>";
				html_val = html_val + "<p style=\"margin:2pt\">" + json_obj[i].author + "</p>";
				html_val = html_val + "<p style=\"margin:2pt\">&#65509;" + json_obj[i].price + "</p>";
				html_val = html_val + "</div>";
			}
			console.log(html_val);
			$('#book_favorite').html(html_val);
		});
	})();

	(function(){
		$.get('/order/count_cart/', {}, function(data){
			$('#base_cart_count').html("购物车(" + data + ")")
			console.log('/order/count_cart/');
		});
	})();

	$('#comment').click(function(){
		var bookid_in;
		var userid_in;
		var orderid_in;
		var score_in;
		var content_in;
		bookid_in = $(this).attr("data-bookid");
		userid_in = $(this).attr("data-userid");
		orderid_in = $(this).attr("data-orderid");
		score_in = $('#score').val()
		content_in = $('#content').val()
		var ret1 = ''
		var ret2 = ''
		$.ajax({
			type: 'GET',
			url: '/book/add_comment/',
			data: {user_id: userid_in, book_id: bookid_in, score: score_in, content: content_in},
			async: false,
			success: function(data) {
				ret1 = data;
			}
		});
		$.ajax({
			type: 'GET',
			url: '/order/modify_order',
			data: {order_id:orderid_in},
			async: false,
			success: function(data) {
				ret2 = data;
			}
		});
        /*
		$.get('/book/add_comment/', {user_id: userid_in, book_id: bookid_in, score: score_in, content: content_in}, function(data){
			//$('#content').val(data)
			ret1 = data
		});
		$.get('/order/modify_order', {order_id:orderid_in}, function(data){
            ret2 = data
		});*/
		console.log('ret1: ' + ret1 + ', ret2: ' + ret2);
		var result = "评价失败";
		if (ret1 == 'ok' && parseInt(ret2) >= 0){
			result = "评价成功";
		}
		var html_val = 
		'    <br>\
		<div class="row">\
			<div class="col-sm-6 col-md-4 col-lg-3 text-center">'
			+ result +
			'</div>\
		</div>\
		<div class="row">\
			<div class="col-sm-6 col-md-4 col-lg-3 text-center">\
				<a class="btn btn-primary" href="http://127.0.0.1:8000/">返回首页</a>\
				<a class="btn btn-primary" href="/book/book/' + bookid_in + '">查看评价</a>\
			</div>\
		</div>';
		$('#comment_body').html(html_val);
	});

	$('#btn_search').click(function(){
		keyword_in = $('#query').val()
		$.get('/book/global_search/', {keyword: keyword_in}, function(data){
			//console.log(data)
			var json_obj = JSON.parse(data);
			var html_val = "</br><div class=\"row\">";
			for (i=0; i<json_obj.length; i++){
				html_val = html_val + "<div class=\"col-sm-6 col-md-4 col-lg-3\" style=\"font-size: 14px\">";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\">";
                html_val = html_val + "<div style=\"width:150px;height:200px;background: url('/media/" + json_obj[i].picture + "') no-repeat center; background-size: contain;\"  alt=\"Picture\" ></div>";
                html_val = html_val + "</a><br>";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\"><strong>" + json_obj[i].name + "</strong></a>";
				html_val = html_val + "<p style=\"margin:2pt\">" + json_obj[i].author + "</p>";
				html_val = html_val + "<p style=\"margin:2pt\">&#65509;" + json_obj[i].price + "</p>";
				html_val = html_val + "</div>";
			}
			html_val = html_val + '</div>';
			//console.log(html_val)
			$('#book_result').html(html_val);
		});
	});

	$('#btn_category_search').click(function(){
		categoryid_in = $('#category_categoryid').val()
		keyword_in = $('#category_query').val()
		$.get('/book/category_search/', {keyword: keyword_in, category_id:categoryid_in}, function(data){
			//console.log(data)
			var json_obj = JSON.parse(data);
			var html_val = "";
			for (i=0; i<json_obj.length; i++){
				html_val = html_val + "<div class=\"col-sm-6 col-md-4 col-lg-3\" style=\"font-size: 14px\">";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\">";
                html_val = html_val + "<div style=\"width:150px;height:200px;background: url('/media/" + json_obj[i].picture + "') no-repeat center; background-size: contain;\"  alt=\"Picture\" ></div>";
                html_val = html_val + "</a><br>";
				html_val = html_val + "<a href=\"/book/book/" + json_obj[i].id + "\"><strong>" + json_obj[i].name + "</strong></a>";
				html_val = html_val + "<p style=\"margin:2pt\">" + json_obj[i].author + "</p>";
				html_val = html_val + "<p style=\"margin:2pt\">&#65509;" + json_obj[i].price + "</p>";
				html_val = html_val + "</div>";
			}
			//console.log(html_val)
			$('#category_book_result').html(html_val)
		})
	});

	$('#book_add_cart').click(function(){
		var bookid_in = $(this).attr("data-bookid");
		var count_in = $('#book_count').val();
		console.log('book_add_cart')
		console.log(bookid_in);
		$.get('/order/add_cart/', {book_id: bookid_in, count: count_in}, function(data){
			$('#base_cart_count').html("购物车(" + data + ")")
		});
	});

	$('#cart_delete').click(function(){
		var bookid_in = $(this).attr("data-id");
		console.log(bookid_in);
		$.get('/order/delete_cart/', {book_id:bookid_in}, function(data){
			location.reload(true);
		});
	});
	
});

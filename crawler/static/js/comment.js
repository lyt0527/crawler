var url = window.location.href;
url = url.substring(0,url.length-1);
//console.log(url);
var para = url.split('?')[1];
//console.log(para);
var library = para.split('&')[0];
//console.log(library);
var timeRange = para.split('&')[1];
//console.log(timeRange);

function initTime(){
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var today = getDate();
	var myDate = new Date();
	if(timeRange == 'month'){
		var start = new Date(myDate.getTime() - 86400000*30);
		var month = Number(start.getMonth()+1);
		if(month<10){
			month = '0' + month;
		}
		var day = Number(start.getDate());
		if(day<10){
			day = '0' + day;
		}
		startTime.value = start.getFullYear()+'-'+month+'-'+day;
		endTime.value = today;
	}
	if(timeRange == 'week'){
		var start = new Date(myDate.getTime() - 86400000*7);
		var month = Number(start.getMonth()+1);
		if(month<10){
			month = '0' + month;
		}
		startTime.value = start.getFullYear()+'-'+month+'-'+start.getDate();
		endTime.value = today;
	}
	if(timeRange == 'day'){
		var start = new Date(myDate.getTime());
		var month = Number(start.getMonth()+1);
		if(month<10){
			month = '0' + month;
		}
		startTime.value = start.getFullYear()+'-'+month+'-'+start.getDate();
		endTime.value = today;
	}
}
window.onload = function(){
	$('.commentDetail:eq(0)').hide();
	$('.commentDetail:eq(1)').hide();
	var userJsonStr = sessionStorage.getItem('jwt');
    if (userJsonStr) {
		var startTime = document.getElementById('startTime');
		var endTime = document.getElementById('endTime');
		var today = getDate();
		startTime.max = today;
		endTime.max = today;
		if(timeRange != undefined){
			initTime();
		}
		var lowScore = document.getElementById('lowScore');
		var highScore = document.getElementById('highScore');
		if((library == 'comment')||(library =='judgement')){
			lowScore.disabled = 'disabled';
			highScore.disabled = 'disabled';
		}

		var orderNo = document.getElementById('orderNo');
		var name = document.getElementById('userName');
		var platform = document.getElementById('platform');
		var tel = document.getElementById('tel');
		var startTime = document.getElementById('startTime');
		var endTime = document.getElementById('endTime');
		var lowScore = document.getElementById('lowScore');
		var highScore = document.getElementById('highScore');
		var replyState = document.getElementById('replyState');
		var allPage = document.getElementById('allPage');
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
			url:'/search/search_all/',// 跳转到 action
			data:{
				currentPage:1,
				library:library,
				orderNo:orderNo.value,
				name:name.value,
				platform:platform.value,
				tel:tel.value,
				startTime:startTime.value,
				endTime:endTime.value,
				lowScore:lowScore.value,
				highScore:highScore.value,
				replyState:replyState.value,

			},
			type:'post',
			cache:false,
			dataType:'json',
			success:function(data){
				if(data.msg =="success"){
					// console.log(data.dic);
					draw_commentList(data.dic);
					allPage.innerText = data.pages;
					var firstNo = document.getElementById('content').children[0].children[6].children[0];
					toCheck(firstNo);
				}
			},
			error:function() {
			}
		});

	}else{
    	alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout"
    }
}

function draw_commentList(data){
	var count = 0;
	var Olist = document.getElementById('content');
	Olist.innerText = '';
	for(count=0;count<data.length;count++){
		var new_row = document.createElement('tr');
		var No = document.createElement('td');
		No.className = 'No';
		var name = document.createElement('td');
		name.className = 'name';
		var platform = document.createElement('td');
		platform.className = 'platform';
		var catchTime = document.createElement('td');
		catchTime.className = 'catchTime';
		var commentTime = document.createElement('td');
		commentTime.className = 'commentTime';
		var score = document.createElement('td');
		score.className = 'score';
		var operation = document.createElement('td');
		var btn = document.createElement('input');
		btn.type = 'button';
		btn.onclick = function(){toCheck(this);}
		operation.className = 'detail';
		
 		No.innerText = data[count].comment_id;
 		// console.log('1111111111111111',data[count].comment_id);
 		name.innerText = data[count].author_realname;
 		platform.innerText = data[count].platform;
 		catchTime.innerText = data[count].catch_time;
 		commentTime.innerHTML = data[count].comment_time;
 		score.innerText = data[count].arti_score;
 		btn.value = '查看';
 		if(catchTime.innerText == 'None'){catchTime.innerText = '---';}
		if(commentTime.innerText == 'None'){commentTime.innerText = '---';}
		if(score.innerText == 'undefined'){score.innerText = '---';}
		if(platform.innerText == ''){platform.innerText = '---';}

//		No.innerText = 1;
//		name.innerText = 2;
//		platform.innerText = 3;
//		catchTime.innerText = 4;
//		commentTime.innerHTML = 5;
//		score.innerText = 6;
//		btn.value = '查看';
		
		operation.appendChild(btn);
		new_row.appendChild(No);
		new_row.appendChild(name);
		new_row.appendChild(platform);
		new_row.appendChild(catchTime);
		new_row.appendChild(commentTime);
		new_row.appendChild(score);
		new_row.appendChild(operation);
		Olist.appendChild(new_row)
	}
}
//上一页
function previous(){
	var current = document.getElementById('currentPage');
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	var allPage = document.getElementById('allPage');
	x = parseInt(current.innerText);
	if (x>1){
		x -= 1;
		current.innerText = x;
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/search/search_all/',// 跳转到 action
		    data:{
				currentPage:Number(current.innerText),
				library:library,
				orderNo:orderNo.value,
				name:name.value,
				platform:platform.value,
				tel:tel.value,
				startTime:startTime.value,
				endTime:endTime.value,
				lowScore:lowScore.value,
				highScore:highScore.value,
				replyState:replyState.value,
		    },
		    type:'post',
		    cache:false,
		    dataType:'json',
		    success:function(data){
		        if(data.msg =="success"){
					draw_commentList(data.dic);
					allPage.innerText = data.pages;
		        }
		    },
		    error:function() {

		    }
		});
	}
	else{
		this.disabled = true
	}
}
//下一页
function next(){
	var current = document.getElementById('currentPage');
	var all = parseInt(document.getElementById('allPage').innerText);
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	var allPage = document.getElementById('allPage');
	x = parseInt(current.innerText);
	if(x<all){
		x += 1;
		current.innerText = x;
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/search/search_all/',// 跳转到 action
		    data:{
				currentPage:Number(current.innerText),
				library:library,
				orderNo:orderNo.value,
				name:name.value,
				platform:platform.value,
				tel:tel.value,
				startTime:startTime.value,
				endTime:endTime.value,
				lowScore:lowScore.value,
				highScore:highScore.value,
				replyState:replyState.value,
		    },
		    type:'post',
		    cache:false,
		    dataType:'json',
		    success:function(data){
		        if(data.msg =="success"){
					draw_commentList(data.dic);
					allPage.innerText = data.pages;
		        }
		    },
		    error:function() {

		    }    
		});
	}
	else{
		this.disabled = true
	}
}
//跳转
function toCertainPage(){
	var targetPage = document.getElementById('targetPage');
	var allPage = document.getElementById('allPage');
	var currentPage = document.getElementById('currentPage');
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	var allPage = document.getElementById('allPage');
	if((Number(targetPage.value)>Number(allPage.innerText))||(targetPage.value<1)){
		alert('请输入合法页数!');
	}
	else{
		currentPage.innerText = targetPage.value;
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/search/search_all/',// 跳转到 action
		    data:{
				currentPage:currentPage.innerText,
				library:library,
				orderNo:orderNo.value,
				name:name.value,
				platform:platform.value,
				tel:tel.value,
				startTime:startTime.value,
				endTime:endTime.value,
				lowScore:lowScore.value,
				highScore:highScore.value,
				replyState:replyState.value,
		    },
		    type:'post',
		    cache:false,
		    dataType:'json',
		    success:function(data){
		        if(data.msg =="success"){
					draw_commentList(data.dic);
					// console.log(data.dic, '1111111')
					allPage.innerText = data.pages;
		        }
		    },
		    error:function() {
		    }    
		});
	}
}

//导出
var DownLoadFile = function (options) {
    var config = $.extend(true, { method: 'post' }, options);
    var $iframe = $('<iframe id="down-file-iframe" />');
    var $form = $('<form target="down-file-iframe" method="' + config.method + '" />');
    $form.attr('action', config.url);
    for (var key in config.data) {
        $form.append('<input type="hidden" name="' + key + '" value="' + config.data[key] + '" />');
    }
    $iframe.append($form);
    $(document.body).append($iframe);
    $form[0].submit();
    $iframe.remove();
}
function fileOut(){
   var orderNo = document.getElementById('orderNo');
   var name = document.getElementById('userName');
   var platform = document.getElementById('platform');
   var tel = document.getElementById('tel');
   var startTime = document.getElementById('startTime');
   var endTime = document.getElementById('endTime');
   var lowScore = document.getElementById('lowScore');
   var highScore = document.getElementById('highScore');
   var replyState = document.getElementById('replyState');
   DownLoadFile({
	    headers : {'Authorization' : sessionStorage.getItem('jwt')},
        url:'/export/export_all/', //请求的url
        data:{
        library:library,
        orderNo:orderNo.value,
        name:name.value,
        platform:platform.value,
        tel:tel.value,
        startTime:startTime.value,
        endTime:endTime.value,
        lowScore:lowScore.value,
        highScore:highScore.value,
        replyState:replyState.value,
      },//要发送的数据
   });
}
function showReply(){
	document.getElementsByClassName('replyBox')[0].style.visibility = 'visible';
	var No = document.getElementById('replyNo');
	// console.log(No.innerText,'11111111111111111111')
	var replyNum = document.getElementById('replyNum');
	var replyName = document.getElementById('replyUserName');
	var replyTel = document.getElementById('replyTel');
	var history = document.getElementById('history');
	var replyContent = document.getElementById('replyContent');
	replyNum.innerText = '';
	replyName.innerText = '';
	replyTel.innerText = '';
	history.value = '';
	replyContent.value = '请输入回访内容...';
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/show_reply/',// 跳转到 action
	    data:{
			No:No.innerText,
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){ 
				replyNum.innerText = data.comment_id;
				replyName.innerText = data.author_realname;
				replyTel.innerText = data.author_tel;
				history.value = data.rep[0].history;
//				replyContent.value = data.replyContent;
	        }else{    
	            
	        }    
	    },    
	    error:function() {
			alert("异常！");    
	    }    
	});
}
function closeReply(){
	document.getElementsByClassName('replyBox')[0].style.visibility = 'hidden';
}
function clearContent(obj){
	if(obj.value == '请输入回访内容...'){
		obj.value = '';
	}
}
function clearConditions(){
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	orderNo.value = '';
	name.value = '';
	tel.value = '';
	startTime.value = '';
	endTime.value = '';
	lowScore.value = '';
	highScore.value = '';
	platform.selectedIndex = 0;
	replyState.selectedIndex = 0;
}
function search(){
    var currentPage = document.getElementById('currentPage');
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	var allPage = document.getElementById('allPage');
	var flag = 1;
	if((Number(lowScore.value)<0)||(Number(highScore.value)>1)||(Number(lowScore.value)>Number(highScore.value))||
		(isNaN(lowScore.value))||(isNaN(highScore.value))){
		flag = 0;
	}
	if(Date.parse(startTime.value)>Date.parse(endTime.value)){
		flag = 0;

	}

	if(flag == 1){
        $.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
            url:'/search/search_all/',// 跳转到 action
            data:{
                currentPage: 1,
                library:library,
                orderNo:orderNo.value,
                name:name.value,
                platform:platform.value,
                tel:tel.value,
                startTime:startTime.value,
                endTime:endTime.value,
                lowScore:lowScore.value,
                highScore:highScore.value,
                replyState:replyState.value,
            },
            type:'post',
            cache:false,
            dataType:'json',
            success:function(data){
                if(data.msg =="success"){
    				allPage.innerText = data.pages;
    				// console.log(data.dic)
                    draw_commentList(data.dic);
                }
            },
            error:function() {
            }
        });
	}
	else{
	    alert("请输入合法搜索条件")
	}

}
function toCheck(obj){
	if(obj != undefined){
    	var No = obj.parentNode.parentNode.children[0].innerText;
	}
	// console.log('11111111111111',No);
// 	if(library == 'judgement'){
// 		var replyNo = document.getElementById('replyNo');
// 		var userName = document.getElementById('commentUserName');
// 		var ID = document.getElementById('replyID');
// 		var tel = document.getElementById('replyTel');
// 		var order = document.getElementById('replyOrder');
// 		var delivery = document.getElementById('replyDelivery');
// 		var service = document.getElementById('replyService');
// 		var product = document.getElementById('replyProduct');
// 		var score = document.getElementById('replyScore');
// 		var commentTime = document.getElementById('replyCommentTime');
// 		var address = document.getElementById('replyAddress');
// 		var content = document.getElementById('commentContent');
// 		var sysScore = document.getElementById('sysScore');
// 		var artiScore = document.getElementById('artiScore');
// //		console.log('judge');
// 		$.ajax({
// 			headers : {'Authorization' : sessionStorage.getItem('jwt')},
// 		    url:'/function/comment_content/',// 跳转到 action
// 		    data:{
// 				id:No,
// 		    },
// 		    type:'post',
// 		    cache:false,
// 		    dataType:'json',
// 		    success:function(data){
// 		        if(data.msg =="success"){
// 		        	// console.log('222222222222222222222',data.dic[0].comment_id);
// 					replyNo.innerText = data.dic[0].comment_id;
// 					userName.innerText = data.dic[0].author_realname;
// 					ID.innerText = data.dic[0].comment_id;
// 					tel.innerText = data.dic[0].tel;
// 					order.innerText = data.dic[0].order_number;
// 					delivery.innerText = data.dic[0].delivery;
// 					service.innerText = data.dic[0].service;
// 					product.innerText = data.dic[0].product;
// 					score.innerText = data.dic[0].comment_score;
// 					commentTime.innerText = data.dic[0].comment_time;
// 					address.innerText = data.dic[0].comment_address;
// 					content.value = data.dic[0].comment_content;
// 					sysScore.innerText = data.dic[0].sys_score;
// 					artiScore.innerText = data.dic[0].arti_score;
// 		        }else{
//
// 		        }
// 		    },
// 		    error:function() {
// 				alert("异常");
// 		    }
// 		});
// 	}
// 	else{
// 		var replyNo = document.getElementById('replyNo');
// 		var userName = document.getElementById('commentUserName');
// 		var ID = document.getElementById('replyID');
// 		var commentTime = document.getElementById('replyCommentTime');
// 		var catchTime = document.getElementById('replyCatchTime');
// 		// var score = document.getElementById('replyScore');
// 		var address = document.getElementById('replyAddress');
// 		var content = document.getElementById('commentContent');
// 		var sysScore = document.getElementById('sysScore');
// 		var artiScore = document.getElementById('artiScore');
// 		$.ajax({
// 			headers : {'Authorization' : sessionStorage.getItem('jwt')},
// 		    url:'/function/comment_content/',// 跳转到 action
// 		    data:{
// 				id:No,
// 		    },
// 		    type:'post',
// 		    cache:false,
// 		    dataType:'json',
// 		    success:function(data){
// 		        if(data.msg =="success"){
// 					catchTime.innerText = data.dic[0].catch_time;
// 					replyNo.innerText = data.dic[0].comment_id;
// 					userName.innerText = data.dic[0].author_realname;
// 					ID.innerText = data.dic[0].comment_id;
// 					// score.innerText = data.dic[0].comment_score;
// 					commentTime.innerText = data.dic[0].comment_time;
// 					address.innerText = data.dic[0].comment_address;
// 					content.value = data.dic[0].comment_content;
// 					sysScore.innerText = data.dic[0].sys_score;
// 					artiScore.innerText = data.dic[0].arti_score;
// 		        }else{
//
// 		        }
// 		    },
// 		    error:function() {
// 				alert("异常");
// 		    }
// 		});
// 	}
	$.ajax({
	headers : {'Authorization' : sessionStorage.getItem('jwt')},
	url:'/function/comment_content/',// 跳转到 action
	data:{
		id:No,
	},
	type:'post',
	cache:false,
	dataType:'json',
	success:function(data){
		if(data.msg =="success"){
			if(data.dic[0].type == '1'){ //1--评价,2--评论
				$('.commentDetail:eq(1)').show();
				$('.commentDetail:eq(0)').hide();
				document.getElementById('replyNo2').innerText=data.dic[0].comment_id;
				document.getElementById('commentUserName2').innerText=data.dic[0].author_realname;
				document.getElementById('replyID2').innerText=data.dic[0].comment_id;
				document.getElementById('replyPlatform2').innerText=data.dic[0].platform;
				document.getElementById('replyTelNum2').innerText=data.dic[0].tel;
				document.getElementById('replyOrder2').innerText=data.dic[0].order_number;
				document.getElementById('replyDelivery2').innerText=data.dic[0].delivery;
				document.getElementById('replyService2').innerText=data.dic[0].service;
				document.getElementById('replyProduct2').innerText=data.dic[0].product;
				document.getElementById('replyScore2').innerText=data.dic[0].comment_score;
				document.getElementById('replyCommentTime2').value=data.dic[0].comment_time;
				document.getElementById('replyAddress2').innerText=data.dic[0].comment_address;
				document.getElementById('commentContent2').innerText=data.dic[0].comment_content;
				document.getElementById('sysScore2').innerText=data.dic[0].sys_score;
				document.getElementById('artiScore2').innerText=data.dic[0].arti_score;
			}
			else if(data.dic[0].type == '2'){
				$('.commentDetail:eq(0)').show();
				$('.commentDetail:eq(1)').hide();
				console.log('11111111111111111',data.dic[0].comment_address);
				document.getElementById('replyNo1').innerText=data.dic[0].comment_id;
				document.getElementById('commentUserName1').innerText=data.dic[0].author_realname;
				document.getElementById('replyID1').innerText=data.dic[0].comment_id;
				document.getElementById('replyPlatform1').innerText=data.dic[0].platform;
				document.getElementById('replyCommentTime1').value=data.dic[0].comment_time;
				document.getElementById('replyCatchTime1').innerText=data.dic[0].catch_time;
				document.getElementById('replyAddress1').innerText=data.dic[0].comment_address;
				document.getElementById('commentContent1').innerText=data.dic[0].comment_content;
				document.getElementById('sysScore1').innerText=data.dic[0].sys_score;
				document.getElementById('artiScore1').innerText=data.dic[0].arti_score;
			}
		}
	},
	error:function() {
		alert("异常");
	}
	});
}
function submitNew(){
	var newScore = document.getElementById('newScore').value;
	var artiScore = document.getElementById('artiScore');
	var No = document.getElementById('replyNo');
//	console.log(No,'111111111111111111')
	if(Number(newScore>=0) && Number(newScore<=1)&& !(isNaN(newScore)) && (newScore != '')){
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/submit_newscore/',// 跳转到 action
		    data:{
				newScore:newScore,
                No:No.innerText,
		    },    
		    type:'post',    
		    cache:false,    
		    dataType:'json',    
		    success:function(data){    
		        if(data.msg =="success"){    
					artiScore.innerText = newScore;
					msgNum();
		        }else{    
		            
		        }    
		    },    
		    error:function() {
				alert("异常！");    
		    }    
		});
	}
	else{
		alert('请输入合法分数!');
	}

}
function submitReply(){
	var content = document.getElementById('replyContent');
	var replyNum = document.getElementById('replyNum');
	var user = sessionStorage.getItem('name');
	if((content.value == '请输入回访内容...')||(content.value == '')){
		alert('请输入回访内容!');
	}
	else{
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/reply/',// 跳转到 action
		    data:{
				No:replyNum.innerText,
				replyContent:content.value,
				name:user,
		    },
		    type:'post',
		    cache:false,
		    dataType:'json',
		    success:function(data){
		        if(data.msg =="success"){
					alert('修改成功!');
		        }else{

		        }
		    },
		    error:function() {
				alert("异常！");
		    }
		});
	}
}
function changeItem(obj){
	// var url = window.location.href;
	// url = url.substring(0,url.length-1);
	// para = url.split('?')[1];
	// // console.log(para);
	// library = para.split('&')[0];
	// console.log(library);
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	var allPage = document.getElementById('allPage');
	// if(library == 'judgement'){
	// 	var replyNo = document.getElementById('replyNo');
	// 	var userName = document.getElementById('commentUserName');
	// 	var ID = document.getElementById('replyID');
	// 	var tel = document.getElementById('replyTel');
	// 	var order = document.getElementById('replyOrder');
	// 	var delivery = document.getElementById('replyDelivery');
	// 	var service = document.getElementById('replyService');
	// 	var product = document.getElementById('replyProduct');
	// 	var score = document.getElementById('replyScore');
	// 	var commentTime = document.getElementById('replyCommentTime');
	// 	var address = document.getElementById('replyAddress');
	// 	var content = document.getElementById('commentContent');
	// 	var sysScore = document.getElementById('sysScore');
	// 	var artiScore = document.getElementById('artiScore');
	// 	$.ajax({
	// 		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	// 	    url:'/function/changeitems/',// 跳转到 action
	// 	    data:{
	// 			No:replyNo.innerText,
	// 			library:library,
	// 			item:obj.value,
	// 			orderNo:orderNo.value,
	// 			name:name.value,
	// 			platform:platform.value,
	// 			tel:tel.value,
	// 			startTime:startTime.value,
	// 			endTime:endTime.value,
	// 			lowScore:lowScore.value,
	// 			highScore:highScore.value,
	// 			replyState:replyState.value,
	// 	    },
	// 	    type:'post',
	// 	    cache:false,
	// 	    dataType:'json',
	// 	    success:function(data){
	// 	        if(data.msg =="success"){
	// 				replyNo.innerText = data.dic[0].comment_id;
	// 				userName.innerText = data.dic[0].author_realname;
	// 				ID.innerText = data.dic[0].comment_id;
	// 				tel.innerText = data.dic[0].tel;
	// 				order.innerText = data.dic[0].order_number;
	// 				delivery.innerText = data.dic[0].delivery;
	// 				service.innerText = data.dic[0].service;
	// 				product.innerText = data.dic[0].product;
	// 				score.innerText = data.dic[0].comment_score;
	// 				commentTime.innerText = data.dic[0].comment_time;
	// 				address.innerText = data.dic[0].catch_address;
	// 				content.value = data.dic[0].comment_content;
	// 				sysScore.innerText = data.dic[0].sys_score;
	// 				artiScore.innerText = data.dic[0].arti_score;
	// 	        }else{
    //
	// 	        }
	// 	    },
	// 	    error:function() {
	// 			alert("异常");
	// 	    }
	// 	});
	// }
	// else{
	// 	var replyNo = document.getElementById('replyNo');
	// 	var userName = document.getElementById('commentUserName');
	// 	var ID = document.getElementById('replyID');
	// 	var commentTime = document.getElementById('replyCommentTime');
	// 	var catchTime = document.getElementById('replyCatchTime');
	// 	var address = document.getElementById('replyAddress');
	// 	var content = document.getElementById('commentContent');
	// 	var sysScore = document.getElementById('sysScore');
	// 	var artiScore = document.getElementById('artiScore');
	// 	$.ajax({
	// 		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	// 	    url:'/function/changeitems/',// 跳转到 action
	// 	    data:{
	// 			No:replyNo.innerText,
	// 			library:library,
	// 			item:obj.value,
	// 			orderNo:orderNo.value,
	// 			name:name.value,
	// 			platform:platform.value,
	// 			tel:tel.value,
	// 			startTime:startTime.value,
	// 			endTime:endTime.value,
	// 			lowScore:lowScore.value,
	// 			highScore:highScore.value,
	// 			replyState:replyState.value,
	// 	    },
	// 	    type:'post',
	// 	    cache:false,
	// 	    dataType:'json',
	// 	    success:function(data){
	// 	        if(data.msg =="success"){
	// 				replyNo.innerText = data.dic[0].comment_id;
	// 				userName.innerText = data.dic[0].author_realname;
	// 				ID.innerText = data.dic[0].comment_id;
	// 				commentTime.innerText = data.dic[0].comment_time;
	// 				catchTime.innerText = data.dic[0].catch_time;
	// 				address.innerText = data.dic[0].catch_address;
	// 				content.value = data.dic[0].comment_content;
	// 				sysScore.innerText = data.dic[0].sys_score;
	// 				artiScore.innerText = data.dic[0].arti_score;
	// 	        }else{
	//
	// 	        }
	// 	    },
	// 	    error:function() {
	// 			alert("异常");
	// 	    }
	// 	});
	// }
	var No = obj.parentNode.parentNode.children[1].children[0].children[1].innerText;
	var orderNo = document.getElementById('orderNo');
	var name = document.getElementById('userName');
	var platform = document.getElementById('platform');
	var tel = document.getElementById('tel');
	var startTime = document.getElementById('startTime');
	var endTime = document.getElementById('endTime');
	var lowScore = document.getElementById('lowScore');
	var highScore = document.getElementById('highScore');
	var replyState = document.getElementById('replyState');
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
		url:'/function/changeitems/',// 跳转到 action
		data:{
			id:No,
			library:library,
			item:obj.value,
			orderNo:orderNo.value,
			name:name.value,
			platform:platform.value,
			tel:tel.value,
			startTime:startTime.value,
			endTime:endTime.value,
			lowScore:lowScore.value,
			highScore:highScore.value,
			replyState:replyState.value,
		},
		type:'post',
		cache:false,
		dataType:'json',
		success:function(data){
			if(data.msg =="success"){
				if(data.dic[0].type == '1'){ //1--评价,2--评论
					$('.commentDetail:eq(1)').show();
					$('.commentDetail:eq(0)').hide();
					document.getElementById('replyNo2').innerText=data.dic[0].comment_id;
					document.getElementById('commentUserName2').innerText=data.dic[0].author_realname;
					document.getElementById('replyID2').innerText=data.dic[0].comment_id;
					document.getElementById('replyPlatform2').innerText=data.dic[0].platform;
					document.getElementById('replyTelNum2').innerText=data.dic[0].tel;
					document.getElementById('replyOrder2').innerText=data.dic[0].order_number;
					document.getElementById('replyDelivery2').innerText=data.dic[0].delivery;
					document.getElementById('replyService2').innerText=data.dic[0].service;
					document.getElementById('replyProduct2').innerText=data.dic[0].product;
					document.getElementById('replyScore2').innerText=data.dic[0].comment_score;
					document.getElementById('replyCommentTime2').value=data.dic[0].comment_time;
					document.getElementById('replyAddress2').innerText=data.dic[0].comment_address;
					document.getElementById('commentContent2').innerText=data.dic[0].comment_content;
					document.getElementById('sysScore2').innerText=data.dic[0].sys_score;
					document.getElementById('artiScore2').innerText=data.dic[0].arti_score;
				}
				else if(data.dic[0].type == '2'){
					$('.commentDetail:eq(0)').show();
					$('.commentDetail:eq(1)').hide();
					document.getElementById('replyNo1').innerText=data.dic[0].comment_id;
					document.getElementById('commentUserName1').innerText=data.dic[0].author_realname;
					document.getElementById('replyID1').innerText=data.dic[0].comment_id;
					document.getElementById('replyPlatform1').innerText=data.dic[0].platform;
					document.getElementById('replyCommentTime1').value=data.dic[0].comment_time;
					document.getElementById('replyCatchTime1').innerText=data.dic[0].catch_time;
					document.getElementById('replyAddress1').innerText=data.dic[0].comment_address;
					document.getElementById('commentContent1').innerText=data.dic[0].comment_content;
					document.getElementById('sysScore1').innerText=data.dic[0].sys_score;
					document.getElementById('artiScore1').innerText=data.dic[0].arti_score;
				}
            }
		},
		error:function() {
			alert("异常");
		}
	});
}
function getDate(){
	var mydate = new Date();
	date = mydate.getDate();
	month = mydate.getMonth();
	month += 1;
	year = mydate.getFullYear();
	if(date<10){
		date = '0' + date;
	}
	if(month<10){
		month = '0' +month;
	}
	today = year+'-'+month+'-'+date;
	return today;
}
function msgNum(){
	var msgNum = window.parent.document.getElementById('msgNum');
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/count/',// 跳转到 action
	    data:{},
	    type:'post',
	    cache:false,
	    dataType:'json',
	    success:function(data){
	        if(data.msg =="success"){
				msgNum.innerText = data.msgNum;
	        }else{
	            msgNum.innerText = '---';
	        }
	    },
	    error:function() {
			alert("异常！");
	    }
	});
}
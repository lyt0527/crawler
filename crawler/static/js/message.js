window.onload = function(){
	var userJsonStr = sessionStorage.getItem('jwt');
	if (userJsonStr) {
		getAllPages();
		// var data = new Array();
		getData();
		// for(var i=0;i<10;i++){
		// 	data.push({
		// 		'warning':'data',
		// 		'ID':13,
		// 		'commentType':'评价',
		// 		'time':'2019-3-18',
		// 		'platform':'XX平台',
		// 		'content':'叽里呱啦',
		// 		'userName':'海娃',
		// 		'star':3,
		// 	});
		// }
	}else{
	alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout"
	}
};
function draw_msgList(data){
	// console.log(data.length);
	var i = 0;
	var Olist = document.getElementById('content');
	Olist.innerText = '';
	for(i=0;i<data.length;i++){
		var new_row = document.createElement('tr');
		var warning = document.createElement('td');
		var pic = document.createElement('img');
		// pic.src = '/static/images/'warning.png';
		warning.appendChild(pic);
		warning.className = 'warning';
		var id = document.createElement('td');
		id.className = 'id';
		var commentType = document.createElement('td');
		commentType.className = 'commentType';
		var time = document.createElement('td');
		time.className = 'time';
		var platform = document.createElement('td');
		platform.className = 'platform';
		var content = document.createElement('td');
		content.className = 'content';
		var user = document.createElement('td');
		user.className = 'user';
		var score = document.createElement('td');
		score.className = 'score';
		var operation = document.createElement('td');
		var btn1 = document.createElement('input');
		var btn2 = document.createElement('input');
		operation.className = 'operation';
		btn1.type = 'button';btn1.className = 'detail';
		btn1.onclick = function(){ showCard(this);}
		btn2.type = 'button';btn2.className = 'ignore';
		btn2.onclick = function(){ ignore(this);}
		
		if(data[i].is_read == '0'){
			pic.src = '/static/images/warning.png';
		}
		id.innerText = data[i].comment_id;
		commentType.innerText = data[i].comment_type;
		time.innerText = data[i].comment_time;
		platform.innerText = data[i].platform;
		if(data[i].comment_content.length > 18){
			data[i].comment_content = data[i].comment_content.substring(0,18)+'······';
		}
		content.innerText = data[i].comment_content;
		user.innerText = data[i].author_realname;
		score.innerText = data[i].comment_star;
		btn1.value = '查看';
		btn2.value = '忽略';
		
		operation.appendChild(btn1);
		operation.appendChild(btn2);
		new_row.appendChild(warning)
		new_row.appendChild(id);
		new_row.appendChild(commentType);
		new_row.appendChild(time);
		new_row.appendChild(platform);
		new_row.appendChild(content);
		new_row.appendChild(user);
		new_row.appendChild(score);
		new_row.appendChild(operation);
		Olist.appendChild(new_row)
	}
}
function previous(){
	var current = document.getElementById('currentPage');
	x = parseInt(current.innerText);
	if (x>1){
		x -= 1;
		current.innerText = x;
		getData();
	}
	else{
		this.disabled = true;
	}	
}

function next(){
	var current = document.getElementById('currentPage');
	var all = parseInt(document.getElementById('allPage').innerText);
	x = parseInt(current.innerText);
	if(x<all){
		x += 1;
		current.innerText = x;
		getData();
	}
	else{
		this.disabled = true;
	}
}
function toCertainPage(){
	var targetPage = document.getElementById('targetPage');
	var allPage = document.getElementById('allPage');
	var currentPage = document.getElementById('currentPage');
	if((Number(targetPage.value)>Number(allPage.innerText))||(targetPage.value<1)){
		alert('请输入合法页数!');
	}
	else{
		currentPage.innerText = targetPage.value;
		getData();
	}
}
function showCard(obj){
	var commentType = obj.parentNode.parentNode.children[2].innerText;
	var id = obj.parentNode.parentNode.children[1].innerText;
	var warning = obj.parentNode.parentNode.children[0].children[0];
	warning.src = '';
	if(commentType == '评论'){
		document.getElementsByClassName('commentDetail')[0].style.visibility = 'visible';
		document.getElementsByClassName('commentDetail')[1].style.visibility = 'hidden';
		document.getElementsByClassName('replyBox')[0].style.visibility = 'hidden';
		details(0,id);
	}
	else{
		document.getElementsByClassName('commentDetail')[1].style.visibility = 'visible';
		document.getElementsByClassName('commentDetail')[0].style.visibility = 'hidden';
		document.getElementsByClassName('replyBox')[0].style.visibility = 'hidden';
		details(1,id);
	}
}
function closeCard(){
	document.getElementsByClassName('commentDetail')[0].style.visibility = 'hidden';
	document.getElementsByClassName('commentDetail')[1].style.visibility = 'hidden';
	document.getElementsByClassName('replyBox')[0].style.visibility = 'hidden';
}
function showReply(obj){
	document.getElementsByClassName('replyBox')[0].style.visibility = 'visible';
	var No = obj.parentNode.parentNode.parentNode.children[1].children[0].children[1].innerText;
	// console.log(obj);
	var replyNo = document.getElementById('replyNo');
	var replyName = document.getElementById('replyName');
	var replyTel = document.getElementById('replyTel');
	var history = document.getElementById('history');
	var replyContent = document.getElementById('replyContent');
	replyNo.innerText = '';
	replyName.innerText = '';
	replyTel.innerText = '';
	history.value = '';
	replyContent.value = '请输入回访内容...';
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/show_reply/',// 跳转到 action
	    data:{
			No:No,
	    },
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){ 
				replyNo.innerText = data.comment_id;
				replyName.innerText = data.author_realname;
                // console.log('ddddddddddddddd',data.comment_id,data.author_realname);
                replyTel.innerText = data.author_tel;
				history.value = data.rep[0].history;
				// replyContent.value = data.replyContent;
	        }else{    
	            console.log('failure!');
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
function getAllPages(){
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/all_page/',// 跳转到 action
	    data:{
			
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){    
				document.getElementById('allPage').innerText = data.allPage;
	        }else{
	            document.getElementById('allPage').innerText = '---';
	        }    
	    },    
	    error:function() {
			alert("异常！");    
	    }    
	});
}
function getData(){
	var currentPage = document.getElementById('currentPage');
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/news/',// 跳转到 action
	    data:{
			currentPage: Number(currentPage.innerText),
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){    
				// console.log(data.low_list);
				draw_msgList(data.low_list);
	        }else{    
	            return '获取失败';
	        }    
	    },    
	    error:function() {
			alert("异常！");    
	    }    
	});
}
function details(type,ID){
	if(type == '0'){
		var No = document.getElementById('commentNo');
		var name = document.getElementById('commentName');
		var id = document.getElementById('commentID');
		var platform = document.getElementById('commentPlatform');
		var commentTime = document.getElementById('commentTime');
		var catchTime = document.getElementById('catchTime');
		var address = document.getElementById('commentAddress');
		var content = document.getElementById('commentContent');
		var sysScore = document.getElementById('commentSysScore');
		var artiScore = document.getElementById('commentArtiScore');
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/comment_content/',// 跳转到 action
		    data:{
				id:ID,
		    },
		    type:'post',
		    cache:false,    
		    dataType:'json',    
		    success:function(data){    
		        if(data.msg =="success"){
		        	// console.log('1111111111111111111',data.dic[0].comment_id);
					No.innerText = data.dic[0].comment_id;
					name.innerText = data.dic[0].author_realname;
					id.innerText = data.dic[0].comment_id;
					platform.innerText = data.dic[0].platform;
					commentTime.innerText = data.dic[0].comment_time;
					catchTime.innerText = data.dic[0].catch_time;
					address.innerText = data.dic[0].comment_address;
					content.innerText = data.dic[0].comment_content;
					sysScore.innerText = data.dic[0].sys_score;
					artiScore.innerText = data.dic[0].arti_score;
		        }else{    
		            No.innerText = '获取失败';
		            name.innerText = '获取失败';
		            id.innerText = '获取失败';
		            commentTime.innerText = '获取失败';
		            catchTime.innerText = '获取失败';
		            address.innerText = '获取失败';
		            content.innerText = '获取失败';
		            sysScore.innerText = '获取失败';
					artiScore.innerText = '获取失败';
		        }    
		    },    
		    error:function() {
				alert("异常！");    
		    }    
		});
	}
	if(type =='1'){
		var No = document.getElementById('judgementNo');
		var name = document.getElementById('judgementName');
		var id = document.getElementById('judgementID');
		var platform = document.getElementById('judgementPlatform');
		var Tel = document.getElementById('judgementTel');
		var order = document.getElementById('judgementDelivery');
		var service = document.getElementById('judgementService');
		var product = document.getElementById('judgementProduct');
		var score = document.getElementById('judgementScore');
		var time = document.getElementById('judgementTime');
		var address = document.getElementById('judgementAddress');
		var content = document.getElementById('judgementContent');
		var sysScore = document.getElementById('judgementSysScore');
		var artiScore = document.getElementById('judgementArtiScore');
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/comment_content/',// 跳转到 action
		    data:{
				id:ID,
		    },    
		    type:'post',    
		    cache:false,    
		    dataType:'json',    
		    success:function(data){    
		        if(data.msg =="success"){
		        	// console.log('2222222222222222222222');
					No.innerText = data.dic[0].comment_id;
					name.innerText = data.dic[0].author_realname;
					id.innerText = data.dic[0].comment_id;
					platform.innerText = data.dic[0].platform;
					Tel.innerText = data.dic[0].tel;
					order.innerText = data.dic[0].order_number;
					service = data.dic[0].service;
					product = data.dic[0].product;
					score = data.dic[0].score;
					time.innerText = data.dic[0].comment_time;
					address.innerText = data.dic[0].comment_address;
					content.innerText = data.dic[0].comment_content;
					sysScore.innerText = data.dic[0].sys_score;
					artiScore.innerText = data.dic[0].arti_score;
		        }else{    
		            No.innerText = '获取失败';
		            name.innerText = '获取失败';
		            id.innerText = '获取失败';
					Tel.innerText = '获取失败';
					order.innerText = '获取失败';
					service = '获取失败';
					product = '获取失败';
		            time.innerText = '获取失败';
		            catchTime.innerText = '获取失败';
		            address.innerText = '获取失败';
		            content.innerText = '获取失败';
		            sysScore.innerText = '获取失败';
					artiScore.innerText = '获取失败';
		        }    
		    },    
		    error:function() {
				alert("异常！");    
		    }    
		});
	}
}
function ignore(obj){
	// console.log('ignore')
	var ID = obj.parentNode.parentNode.children[1].innerText;
	var warning = obj.parentNode.parentNode.children[0].children[0];
	warning.src = '';
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/is_ignore/',// 跳转到 action
	    data:{
			id:ID,
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){    
				
	        }else{    
	            
	        }    
	    },    
	    error:function() {
			alert("异常！");    
	    }    
	});
}
function submitNew(obj){
	var newScore = obj.parentNode.children[1].value;
	var artiScore = obj.parentNode.parentNode.children[1].children[3];
	var No = obj.parentNode.parentNode.parentNode.children[1].children[0].children[1].innerText;
	if(Number(newScore>=0) && Number(newScore<=1)&& !(isNaN(newScore)) && (newScore != '')){
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/submit_newscore/',// 跳转到 action
		    data:{
				newScore:newScore,
				No:No,
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
	else {
        alert('请输入合法分数!');
    }

}
function clearContent(obj){
	if(obj.value == '请输入回访内容...'){
		obj.value = '';
	}
}

function submitReply(){
	var content = document.getElementById('replyContent');
	var replyNo = document.getElementById('replyNo');
	var user = sessionStorage.getItem('name');
	if((content.value == '请输入回访内容...')||(content.value == '')){
		alert('请输入回访内容!');
	}
	else{
	    $.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
            url:'/function/reply/',// 跳转到 action
            data:{
                No:replyNo.innerText,
                replyContent:content.value,
				name:user,
            },
            type:'post',
            cache:false,
            dataType:'json',
            success:function(data){
                if(data.msg =="success"){
                    alert('修改成功!');
                }
                else{

                }
            },
            error:function() {
                alert("异常！");
            }
        });
	}
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
	        	// console.log(data.msg,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmm');
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
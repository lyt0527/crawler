var picName = new Array();
picName['主页'] = 'index';
picName['高分库'] = 'high';
picName['低分库'] = 'low';
picName['评论待处理'] = 'comment';
picName['评价待处理'] = 'judgement';
picName['训练模型'] = 'train';
picName['系统重新评分'] = 'rejudge';
window.onload = function(){
	var userJsonStr = sessionStorage.getItem('jwt');
	if (userJsonStr){
		var userName = document.getElementById('userName');
		userName.innerText = sessionStorage.getItem('name');
		var msgNum = document.getElementById('msgNum');
		var url = window.location.href;
		var userid = url.split("=")[1][0];
		$.ajax({
			url:'/function/count/',// 跳转到 action
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
			data:{
				userid:userid,
			},
			type:'post',
			cache:false,
			dataType:'json',
			success:function(data){
				if(data.msg =="success"){
					userName.innerText = data.userName;
					msgNum.innerText = data.msgNum;
				}else{
					userName.innerText = '用户名';
					msgNum.innerText = '--';
				}
			},
			error:function() {
				alert("异常！");
			}
		});}else{
			alert("你没有权限访问，请与管理员联系。");
			window.location.href = "/account/logout"
	}
};
var checked = [1,0,0,0,0,0,0];
function changeAfterClick(obj){
	for(var i=0;i<7;i++){checked[i] = 0;}
	checked[$(obj).index('li')] = 1;
	var listOfNav = document.getElementsByTagName('li');
	for(var i=0;i<listOfNav.length;i++){
		listOfNav[i].style.backgroundColor = 'white';
		listOfNav[i].style.color = '#333333';
		listOfNav[i].children[0].src = '/static/images/'+picName[listOfNav[i].innerText]+'.png';
	}
	obj.style.backgroundColor = '#29DACC';
	obj.style.color = 'white';
	obj.children[0].src = '/static/images/'+picName[obj.innerText]+'_01.png';
	var frame = document.getElementById('frame');
	switch(obj.innerText){
		case '主页':frame.src = '/function/index/';break;
		case '高分库':frame.src = '/function/comment/?high/';break;
		case '低分库':frame.src = '/function/comment/?low/';break;
		case '评论待处理':frame.src = '/function/comment/?comment/';break;
		case '评价待处理':frame.src = '/function/judgement/?judgement/';break;
		case '训练模型':frame.src = '/function/train/';break;
		case '系统重新评分':frame.src = '/function/rejudge/';break;
	}
}
function mouseover(obj){
	obj.style.backgroundColor = '#29DACC';
	obj.style.color = 'white';
	obj.children[0].src = '/static/images/'+picName[obj.innerText]+'_01.png';
}
function mouseout(obj){
	if(checked[$(obj).index('li')] != 1 ){
		obj.style.backgroundColor = 'white';
		obj.style.color = '#333333';
		obj.children[0].src = '/static/images/'+picName[obj.innerText]+'.png';
	}
}
function tomessage(){
	var frame = document.getElementById('frame');
	frame.src = '/function/message/';
}
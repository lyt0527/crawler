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
	if (userJsonStr) {
		document.getElementById('dateStart').value = getDate();
		document.getElementById('dateEnd').value = getDate();
		var startTime = document.getElementById('dateStart');
		var endTime = document.getElementById('dateEnd');
		var today = getDate();
		startTime.max = today;
		endTime.max = today;

		var typeList = document.getElementsByClassName('typeList')[0].children;
		typeList[0].flag = 1;
		for(var i=1;i<typeList.length;i++){
			typeList[i].flag = 0;
		}
		confirmDate();
		everyItems();
	}else{
		alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout"
    }
	};

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
// function getDate(){
// 	document.getElementById('date1').innerText = yyesterday.getFullYear()+'年'+Number(yyesterday.getMonth()+1)+'月'+yyesterday.getDate()+'日';
// 	document.getElementById('date2').innerText = yesterday.getFullYear()+'年'+Number(yesterday.getMonth()+1)+'月'+yesterday.getDate()+'日';
// 	document.getElementById('date3').innerText = today.getFullYear()+'年'+Number(today.getMonth()+1)+'月'+today.getDate()+'日';
// 	document.getElementById('date4').innerText = tomorrow.getFullYear()+'年'+Number(tomorrow.getMonth()+1)+'月'+tomorrow.getDate()+'日';
// 	document.getElementById('date5').innerText = ttomorrow.getFullYear()+'年'+Number(ttomorrow.getMonth()+1)+'月'+ttomorrow.getDate()+'日';
// }
// function datePlus(){
// 	yyesterday = new Date(yyesterday.getTime()+86400000);
// 	yesterday = new Date(yesterday.getTime()+86400000);
// 	today = new Date(today.getTime()+86400000);
// 	tomorrow = new Date(tomorrow.getTime()+86400000);
// 	ttomorrow = new Date(ttomorrow.getTime()+86400000);
// 	document.getElementById('date1').innerText = yyesterday.getFullYear()+'年'+Number(yyesterday.getMonth()+1)+'月'+yyesterday.getDate()+'日';
// 	document.getElementById('date2').innerText = yesterday.getFullYear()+'年'+Number(yesterday.getMonth()+1)+'月'+yesterday.getDate()+'日';
// 	document.getElementById('date3').innerText = today.getFullYear()+'年'+Number(today.getMonth()+1)+'月'+today.getDate()+'日';
// 	document.getElementById('date4').innerText = tomorrow.getFullYear()+'年'+Number(tomorrow.getMonth()+1)+'月'+tomorrow.getDate()+'日';
// 	document.getElementById('date5').innerText = ttomorrow.getFullYear()+'年'+Number(ttomorrow.getMonth()+1)+'月'+ttomorrow.getDate()+'日';
// }
// function dateMinus(){
// 	yyesterday = new Date(yyesterday.getTime()-86400000);
// 	yesterday = new Date(yesterday.getTime()-86400000);
// 	today = new Date(today.getTime()-86400000);
// 	tomorrow = new Date(tomorrow.getTime()-86400000);
// 	ttomorrow = new Date(ttomorrow.getTime()-86400000);
// 	document.getElementById('date1').innerText = yyesterday.getFullYear()+'年'+Number(yyesterday.getMonth()+1)+'月'+yyesterday.getDate()+'日';
// 	document.getElementById('date2').innerText = yesterday.getFullYear()+'年'+Number(yesterday.getMonth()+1)+'月'+yesterday.getDate()+'日';
// 	document.getElementById('date3').innerText = today.getFullYear()+'年'+Number(today.getMonth()+1)+'月'+today.getDate()+'日';
// 	document.getElementById('date4').innerText = tomorrow.getFullYear()+'年'+Number(tomorrow.getMonth()+1)+'月'+tomorrow.getDate()+'日';
// 	document.getElementById('date5').innerText = ttomorrow.getFullYear()+'年'+Number(ttomorrow.getMonth()+1)+'月'+ttomorrow.getDate()+'日';
// }

function draw_diagram(data){
	var diagram = echarts.init(document.getElementById('diagram'));
	var dateList = data.dateList;
	option = {
		tooltip: {
			trigger: 'axis'
		},
		legend: {
			data:['总数','充电平台','二手车平台','客服系统','E+优品商城','体验小程序','官方商城','服务系统'],
			x:'right'
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: {
			type: 'category',
			//boundaryGap: false,
			data:dateList, 
		},
		yAxis: {
			type: 'value',
			splitLine:{show: false},
		},
		series: [{
            name:'总数',
            type:'line',
			smooth:'true',
            data:data.sum,
        },
        {
            name:'充电平台',
            type:'line',
			smooth:'true',
            data:data.charge,
        },
		{
		    name:'二手车平台',
		    type:'line',
			smooth:'true',
		    data:data.secondHand,
		},
		{
		    name:'客服系统',
		    type:'line',
			smooth:'true',
		    data:data.customer,
		},
		{
		    name:'E+优品商城',
		    type:'line',
			smooth:'true',
		    data:data.Eplus,
		},
		{
		    name:'体验小程序',
		    type:'line',
			smooth:'true',
		    data:data.experience,
		},
		{
		    name:'官方商城',
		    type:'line',
			smooth:'true',
		    data:data.mall
		},
		{
		    name:'服务系统',
		    type:'line',
			smooth:'true',
		    data:data.service,
		},]
	};
	diagram.setOption(option);
}

function listOperation2(obj){
	var list = obj.parentNode.children;
	for(var i=0;i<list.length;i++){
		list[i].style.color = '#333333';
		list[i].flag = 0;
	}
	obj.style.color = '#29DACC';
	obj.flag = 1;
	confirmDate();
}
function confirmDate(){
	var dateStart = document.getElementById('dateStart');
	var dateEnd = document.getElementById('dateEnd');
	var flag = 1;
	var today = getDate();
	var typeList = document.getElementsByClassName('typeList')[0].children;
	for(var i=0;i<typeList.length;i++){
		if(typeList[i].flag == 1){
			var type = i;break;
		}
	}
	// console.log(dateStart.value);
	if(Date.parse(dateStart.value)>Date.parse(dateEnd.value)){
		flag = 0;
	}
	if(flag == 0){
		alert('请选择正确的时间范围!');
	}
	else{
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
		    url:'/function/plotting/',// 跳转到 action
		    data:{
				type:type,
				startTime:dateStart.value,
				endTime:dateEnd.value,
		    },    
		    type:'post',    
		    cache:false,    
		    dataType:'json',    
		    success:function(data){    
		        if(data.msg =="success"){
		        	// console.log(data);
					draw_diagram(data);
		        }else{    
		             
		        }    
		    },    
		    error:function() {
				alert("异常");    
		    }    
		});
	}
}
var checked = parent.checked;
function todetail(obj){
	var library = obj.parentNode.parentNode.children[0].innerText;
	var time = obj.parentNode.children[0].innerText;
	var targetPage = '';
	var nav = window.parent.document.getElementsByClassName('nav')[0].children[0];
	switch(time){
		case '一个月':time = 'month';break;
		case '一周':time = 'week';break;
		case '今天':time = 'day';break;
	}
	switch(library){
		case '低分库':{
			targetPage = '/function/comment?low';
			for(var i=0;i<7;i++){checked[i] = 0;}
			checked[2] = 1;
			for(var i=0;i<7;i++){
				nav.children[i].style.backgroundColor = 'white';
				nav.children[i].style.color = '#333333';
				nav.children[i].children[0].src = '/static/images/'+picName[nav.children[i].innerText]+'.png';
			}
			nav.children[2].style.backgroundColor = '#29DACC';
			nav.children[2].style.color = 'white';
			nav.children[2].children[0].src = '/static/images/'+picName[nav.children[2].innerText]+'_01.png';
		}break;
		case '高分库':{
			targetPage = '/function/comment?high';
			for(var i=0;i<7;i++){checked[i] = 0;}
			checked[1] = 1;
			for(var i=0;i<7;i++){
				nav.children[i].style.backgroundColor = 'white';
				nav.children[i].style.color = '#333333';
				nav.children[i].children[0].src = '/static/images/'+picName[nav.children[i].innerText]+'.png';
			}
			nav.children[1].style.backgroundColor = '#29DACC';
			nav.children[1].style.color = 'white';
			nav.children[1].children[0].src = '/static/images/'+picName[nav.children[1].innerText]+'_01.png';
		}break;
		case '评论待处理':{
			targetPage = '/function/comment?comment';
			for(var i=0;i<7;i++){checked[i] = 0;}
			checked[3] = 1;
			for(var i=0;i<7;i++){
				nav.children[i].style.backgroundColor = 'white';
				nav.children[i].style.color = '#333333';
				nav.children[i].children[0].src = '/static/images/'+picName[nav.children[i].innerText]+'.png';
			}
			nav.children[3].style.backgroundColor = '#29DACC';
			nav.children[3].style.color = 'white';
			nav.children[3].children[0].src = '/static/images/'+picName[nav.children[3].innerText]+'_01.png';
		}break;
		case '评价待处理':{
			targetPage = '/function/judgement?judgement';
			for(var i=0;i<7;i++){checked[i] = 0;}
			checked[4] = 1;
			for(var i=0;i<7;i++){
				nav.children[i].style.backgroundColor = 'white';
				nav.children[i].style.color = '#333333';
				nav.children[i].children[0].src = '/static/images/'+picName[nav.children[i].innerText]+'.png';
			}
			nav.children[4].style.backgroundColor = '#29DACC';
			nav.children[4].style.color = 'white';
			nav.children[4].children[0].src = '/static/images/'+picName[nav.children[4].innerText]+'_01.png';
		};break;
	}
	window.location.href = targetPage+'&'+time+'/';
}
function everyItems(){
	var commentMonth = document.getElementById('commentMonth');
	var commentWeek = document.getElementById('commentWeek');
	var commentToday = document.getElementById('commentToday');
	var judgementMonth = document.getElementById('judgementMonth');
	var judgementWeek = document.getElementById('judgementWeek');
	var judgementToday = document.getElementById('judgementToday');
	var highMonth = document.getElementById('highMonth');
	var highWeek = document.getElementById('highWeek');
	var highToday = document.getElementById('highToday');
	var lowMonth = document.getElementById('lowMonth');
	var lowWeek = document.getElementById('lowWeek');
	var lowToday = document.getElementById('lowToday');
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/count_day/',// 跳转到 action
	    data:{
			
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){    
				commentMonth.innerText = data.commentMonth;
				commentWeek.innerText = data.commentWeek;
				commentToday.innerText = data.commentToday;
				judgementMonth.innerText = data.judgementMonth;
				judgementWeek.innerText = data.judgementWeek;
				judgementToday.innerText = data.judgementToday;
				highMonth.innerText = data.highMonth;
				highWeek.innerText = data.highWeek;
				highToday.innerText = data.highToday;
				lowMonth.innerText = data.lowMonth;
				lowWeek.innerText = data.lowWeek;
				lowToday.innerText = data.lowToday;
	        }else{
	             
	        }    
	    },    
	    error:function() {
			alert("异常");    
	    }    
	});
}
window.onload = function(){
	var userJsonStr = sessionStorage.getItem('jwt');
	if (userJsonStr) {
		var progress = document.getElementsByClassName('progress');
		progress[0].style.visibility = 'visible';
		progress[1].style.visibility = 'hidden';
		progress[2].style.visibility = 'hidden';
		var rightRateLast = document.getElementById('rightRateLast');
		var allLast = document.getElementById('allLast');
		var rightNumLast = document.getElementById('rightNumLast');
		var wrongNumLast = document.getElementById('wrongNumLast');
		var lastTime = document.getElementById('lastTime');
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
			url:'/function/last_rejudge/',// 跳转到 action
			data:{

			},
			type:'post',
			cache:false,
			dataType:'json',
			success:function(data){
				if(data.msg =="success"){
					rightRateLast.innerText = data.last_rate;
					allLast.innerText = data.last_sum;
					rightNumLast.innerText = data.last_correct;
					wrongNumLast.innerText = data.last_wrong;
					lastTime.innerText = data.last_sys_time;
				}else{
					rightRateLast.innerText = '获取失败';
					allLast.innerText = '获取失败';
					rightNumLast.innerText = '获取失败';
					wrongNumLast.innerText = '获取失败';
					lastTime.innerText = '获取失败';
				}
			},
			error:function() {
				alert("异常！");
			}
		});
	}else{
		alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout"
	}
}
var userJsonStr = sessionStorage.getItem('jwt');
if (userJsonStr) {
	function rejudge(){
		var progress = document.getElementsByClassName('progress');
		progress[0].style.visibility = 'hidden';
		progress[1].style.visibility = 'visible';
		progress[2].style.visibility = 'hidden';
		var rightRateLast = document.getElementById('rightRateLast');
		var allLast = document.getElementById('allLast');
		var rightNumLast = document.getElementById('rightNumLast');
		var wrongNumLast = document.getElementById('wrongNumLast');
		var lastTime = document.getElementById('lastTime');
		var rightRateNow = document.getElementById('rightRateNow');
		var allNow = document.getElementById('allNow');
		var rightNumNow = document.getElementById('rightNumNow');
		var wrongNumNow = document.getElementById('wrongNumNow');
		var justnow = document.getElementById('justnow');
		$.ajax({
			headers : {'Authorization' : sessionStorage.getItem('jwt')},
			url:'/function/precision/',// 跳转到 action
			data:{

			},
			type:'post',
			cache:false,
			dataType:'json',
			success:function(data){
				if(data.msg =="success"){
					rightRateLast.innerText = data.last_rate;
					allLast.innerText = data.last_sum;
					rightNumLast.innerText = data.last_correct;
					wrongNumLast.innerText = data.last_wrong;
					lastTime.innerText = data.last_sys_time;
					rightRateNow.innerText = data.pre_rate;
					allNow.innerText = data.pre_sum;
					rightNumNow.innerText = data.pre_correct;
					wrongNumNow.innerText = data.pre_wrong;
					justnow.innerText = data.pre_time;
					progress[0].style.visibility = 'hidden';
					progress[1].style.visibility = 'hidden';
					progress[2].style.visibility = 'visible';
				}else{
					rightRateLast.innerText = '获取失败';
					allLast.innerText = '获取失败';
					rightNumLast.innerText = '获取失败';
					wrongNumLast.innerText = '获取失败';
					lastTime.innerText = '获取失败';
					rightRateNow.innerText = '获取失败';
					allNow.innerText = '获取失败';
					rightNumNow.innerText = '获取失败';
					wrongNumNow.innerText = '获取失败';
					justnow.innerText = '获取失败';
					progress[0].style.visibility = 'hidden';
					progress[1].style.visibility = 'hidden';
					progress[2].style.visibility = 'visible';
				}
			},
			error:function() {
				alert("异常！");
				progress[0].style.visibility = 'visible';
				progress[1].style.visibility = 'hidden';
				progress[2].style.visibility = 'hidden';
			}
		});
	}}else{
		alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout/"

}
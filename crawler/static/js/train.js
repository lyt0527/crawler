window.onload = function(){
	var userJsonStr = sessionStorage.getItem('jwt');
    if (userJsonStr) {
		var tips = document.getElementsByClassName('tips');
		tips[1].style.visibility = 'hidden';
		tips[2].style.visibility = 'hidden';
	}else{
    	alert("你没有权限访问，请与管理员联系。");
		window.location.href = "/account/logout"
    }
}
function train(){
	var tips = document.getElementsByClassName('tips');
	tips[0].style.visibility = 'hidden';
	tips[1].style.visibility = 'visible';
	$.ajax({
		headers : {'Authorization' : sessionStorage.getItem('jwt')},
	    url:'/function/save_train/',// 跳转到 action
	    data:{
			
	    },    
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){
				tips[1].style.visibility = 'hidden';
				tips[2].style.visibility = 'visible';
	        }else{    
	            
	        }    
	    },    
	    error:function() {
			alert("异常！");
			tips[0].style.visibility = 'visible';
			tips[1].style.visibility = 'hidden';
			tips[2].style.visibility = 'hidden';
	    }    
	});
}
function returnBack(){
	var tips = document.getElementsByClassName('tips');
	tips[2].style.visibility = 'hidden';
	tips[0].style.visibility = 'visible';
}
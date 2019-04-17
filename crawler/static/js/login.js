window.onload = function(){
		sessionStorage.clear();
};
function clearContent(obj){
	if(obj.value == '登录账号'){
		obj.value = '';
		obj.style.color = '#808080';
	}
	if(obj.value == '登录密码'){
		obj.value = '';
		obj.type = 'password';
		obj.style.color = '#808080';
	}
}
function login(){
	var account = document.getElementById('account');
	sessionStorage.setItem('name',account.value);
	var password = document.getElementById('password');
	$.ajax({
	    url:'/account/api/v1/login/',// 跳转到 action
	    data:{
			username:account.value,
			password:password.value,
	    },
		async : false,
	    type:'post',    
	    cache:false,    
	    dataType:'json',    
	    success:function(data){    
	        if(data.msg =="success"){
	        	sessionStorage.setItem('jwt', JSON.stringify(data.token));
	        	username = data.username;
				userid = data.user_id;
				window.location.href = "/function/navigator/" + "?uid=" + userid+"/";
				// window.location.href = "http://127.0.0.1:8000/function/navigator/";
				// window.location.href = "http://127.0.0.1:8000/function/index/";
	        }else{
	            alert('账号或密码错误!')
                // window.location.href = "http://127.0.0.1:8000/account/logout/"
	        }
	    },    
	    error:function() {
			// alert("异常！");
			alert("账号或密码错误!");
			window.location.href = "/account/logout/"
	    }    
	});
}
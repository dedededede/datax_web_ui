$(function(){
	$(".tab_title li").click(function(){
	$(".manage_contentRight").hide();
   var index1 = $(this).index();
	 $(this).addClass("current").siblings().removeClass("current");
   $(".tab_content").eq(index1).show().siblings(".tab_content").hide();
	});
	$(".manageaddBtn_container").click(function(){ 
		$('.manage_table').append("<tr><td><input type=\"text\" ></td><td><input type=\"text\" ></td>"+
	         "<td><input type=\"text\" ></td><td><input type=\"text\" ></td>"+
	         "<td><input type=\"text\" ></td><td><input type=\"text\" ></td>"+
	         "<td><input type=\"text\" ></td><td><input type=\"text\" ></td></tr>");
	});
});
 

function getUserList() {
	var memberId = document.getElementById("MemberId").value;
	alert(memberId);
	AjaxUtil.request({
		url : "user/discountRate",
		params : {
			userid : memberId
		},
		type : 'json',
		callback : setMemberdiscountRateprocess
	});

}
function addInfoIntoTable(json) {
	document.getElementById("MemberdiscountRate").setAttribute("value",
			json.discountRate);
}
 
//queryType 1:查询需要审查的注册用户
// 2:获取所有可管理的用户列表    审查用户
function getRegisterUserInfo(queryType, pageNum, name, tableId) { //获取用户列表
	/* alert("getUserInfo" + "|" + queryType + "|" + pageNum + "|" + name
			+ "|" + tableId); */
	AjaxUtil.request({
		url : "user/getuserlist",
		method : "post",
		params : {
			data : JSON.stringify({
				"queryType" : queryType,
				"pageNum" : pageNum,
				"name" : name
			})
		},
		type : 'json',
		callback : fillTable
	});
};

function fillTable(jsondata) { //将用户填充到表格中
	var json = JSON.parse(jsondata.mess);
	$('#register_table').empty();
	$('#register_table').append(
			"<tr><th>用户名</th><th>姓名</th><th>角色</th><th>手机号</th><th>邮箱</th>"
					+ "<th>地址</th><th>职位</th><th>审核结果</th></tr>");
	//alert(json.length);// 
	for (var i = 0; i < json.length; i++) {
		
		$('#register_table')
				.append(
						"<tr>"
								+ "<td>"
								+ json[i].userID
								+ "</td>"
								+ "<td>"
								+ json[i].name
								+ "</td>"
								+ "<td>"
								+ json[i].groupId
								+ "</td>"
								+ "<td>"
								+ json[i].mobile
								+ "</td>"
								+ "<td>"
								+ json[i].email
								+ "</td>"
								+ "<td>"
								+ json[i].address
								+ "</td>"
								+ "<td>"
								+ json[i].department
								+ "</td>"
								+ "<td><select autocomplete=\"off\"><option value=0 >未通过</option><option value=1 selected = \"selected\">通过</option></select></td></tr>");
	};
};


function insureRegisterInfo(){
	var array=[];
	var rows = document.getElementById("register_table").rows.length;
	for (var i = 0; i < rows; i++) { 
		var tarray=[];
		idValue = document.getElementById("register_table").rows[i].cells[0].innerHTML;
		tarray.push(idValue);
		activeValue = document.getElementById("register_table").rows[i].cells[7].innerHTML;
		tarray.push(activeValue);
		array.push(tarray);
	}
	 
	AjaxUtil.request({
		url : "user/activeuserlist",
		method : "post",
		params : {
			data : JSON.stringify({
				"insureRegisterInfo" : array,
			})
		},
		type : 'json',
		callback : refreshRegisterInfo
	}); 
};
function refreshRegisterInfo(){
	getRegisterUserInfo(1, 0, '', 'register_table');
};

 

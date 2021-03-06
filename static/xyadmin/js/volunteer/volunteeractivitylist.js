layui.use(['form','layer','table','laytpl','laydate'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        laytpl = layui.laytpl,
        laydate = layui.laydate,
        table = layui.table;
    //常规用法
    laydate.render({
        elem: '#start_time'
    });
    laydate.render({
        elem: '#end_time'
    });

    function getNowFormatDate() {
        var date = new Date();
        var seperator1 = "-";
        var seperator2 = ":";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        if (month >= 1 && month <= 9) {
            month = "0" + month;
        }
        if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
        }
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
        return currentdate;
    }



    //活动状态
    function checkTime(stime, etime) {
        //开始时间
        var arrs = stime.split(" ")[0].split("-");
        var startTime = new Date(arrs[0], arrs[1]-1, arrs[2]);
        // var startTimes = startTime.getTime();
        //结束时间
        var arre = etime.split(" ")[0].split("-");
        var endTime = new Date(arre[0], arre[1]-1, arre[2]);
        // var endTimes = endTime.getTime();
        //当前时间
        var thisDate = new Date();
        var thisDates = thisDate.getFullYear() + "-" + (thisDate.getMonth() + 1) + "-" + thisDate.getDate();
        var arrn = thisDates.split("-");
        var nowTime = new Date(arrn[0], arrn[1]-1, arrn[2]);
        // var nowTimes = nowTime.getTime();

        var nowTimes = getNowFormatDate();
        var startTimes= stime;
        var endTimes = etime;
        if (nowTimes < startTimes) {
            return '未开始';
        }
        else if (nowTimes > endTimes) {
            return '已结束';
        }
        else {
            return '进行中';
        }
    }

    //活动列表
    var tableIns = table.render({
        elem: '#activityList',
        url : '/xyadmin/volunteer/volunteeractivitylist_data',
        cellMinWidth : 95,
        cellMinHeight:120,
        page : true,
        height : "full-125",
        limits : [10,15,20,25],
        limit : 20,
        id : "activityListTable",
        cols : [[
            {type: "checkbox", fixed:"left"},
            {field: 'id', title: 'ID', width:80, align:"center"},
            {field: 'volunteer__id', title: '编号', width:80, align:"center"},
            {field: 'title', title: '活动名称', align:'center',minWidth:200},
            {field: 'activity_type', title: '活动类型', align:'center',minWidth:100},
            {field: 'volunteer__real_name', title: '姓名', minWidth:100, align:"center"},
            {field: 'volunteer__mobile', title: '手机号', minWidth:150, align:"center"},
            {field: 'status', title: '状态', minWidth:100, align:"center",templet:function (d) {
                    if(d.status == "1"){
                        return "已审核";
                    }
                    if(d.status == "0"){
                        return "未审核";
                    }
                }},
            {field: 'volunteer__volunteer_type', title: '志愿者类型', minWidth:100, align:"center",templet:function (d) {
                    if(d.volunteer__volunteer_type == "1"){
                        return "日常志愿者";
                    }
                    if(d.volunteer__volunteer_type == "2"){
                        return "多媒体志愿者";
                    }
                    if(d.volunteer__volunteer_type == "3"){
                        return "亲子志愿者";
                    }
                    if(d.volunteer__volunteer_type == "4"){
                        return "寒暑假志愿者";
                    }
                }},
            {field: 'activity_place', title: '地点', align:'center',minWidth:200},
            {field: 'start_time', title: '开始时间', align:'center',minWidth:200},
            {field: 'end_time', title: '结束时间', align:'center',minWidth:200},
            // {field: 'publish_time', title: '发布时间', align:'center',minWidth:200},
            // {title: '操作', minWidth:250, templet:'#activityListBar',fixed:"right",align:"center"}
        ]]
    });

    //搜索
    $(".search_btn").on("click",function(){
        table.reload("activityListTable",{
            page: {
                curr: 1 //重新从第 1 页开始
            },
            where: {
                type:$(".type").val(),
                key: $(".searchVal").val(),  //搜索的关键字
                start_time:$(".start_time").val(),
                end_time:$(".end_time").val(),
                status:$(".status").val()
            }
        })
    });


    //删除
    $(".delAll_btn").click(function(){
        var checkStatus = table.checkStatus('userListTable'),
            data = checkStatus.data,
            ids = [];
        if(data.length > 0) {
            for (var i in data) {
                ids.push(data[i].id);
            }
            layer.confirm('确定删除选中的用户？', {icon: 3, title: '提示信息'}, function (index) {
                $.ajax({
                    type:'post',
                    url:'activity_delete',
                    traditional:true,
                    data:{ids : ids,csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
                    dataType: "json",
                    async:false,
                    success:function(data){
                        tableIns.reload();
                        layer.close(index);
                    }
                })
            })
        }else{
            layer.msg("请选择需要删除的用户");
        }
    })

    //活动开始
    $(".activitystatus_btn").click(function(){
        activitystatus('true');
    })
    //活动结束
    $("._activitystatus_btn").click(function(){
        activitystatus('false');
    })
    function activitystatus(status_value){
        var confirm_str=status_value=="true"?"通过审批":"拒绝审批";
        var checkStatus = table.checkStatus('activityListTable'),
            data = checkStatus.data,
            ids = [];
        if(data.length > 0) {
            for (var i in data) {
                ids.push(data[i].id);
            }
            layer.confirm(confirm_str, {icon: 3, title: '提示信息'}, function (index) {
                $.ajax({
                    type:'post',
                    url:'volunteeractivity_check',
                    traditional:true,
                    data:{ids : ids,status:status_value,csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
                    dataType: "json",
                    async:false,
                    success:function(data){
                        tableIns.reload();
                        layer.close(index);
                    }
                })
            })
        }else{
            layer.msg("请选择活动");
        }
    }

    //推荐
    $(".recmdActivity_btn").click(function(){
        recmdActivity('true');
    })
    //不推荐
    $("._recmdActivity_btn").click(function(){
        recmdActivity('false');
    })
    function recmdActivity(recmd_value){
        var confirm_str=recmd_value=="true"?"确定推荐此活动吗":"确定取消推荐此活动吗";
        var checkStatus = table.checkStatus('activityListTable'),
            data = checkStatus.data,
            ids = [];
        if(data.length > 0) {
            for (var i in data) {
                ids.push(data[i].id);
            }
            layer.confirm(confirm_str, {icon: 3, title: '提示信息'}, function (index) {
                $.ajax({
                    type:'post',
                    url:'activity_recmd',
                    traditional:true,
                    data:{ids : ids,recmd:recmd_value,csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()},
                    dataType: "json",
                    async:false,
                    success:function(data){
                        tableIns.reload();
                        layer.close(index);
                    }
                })
            })
        }else{
            layer.msg("请选择活动");
        }
    }

    //活动列表导出
    $(".export_btn").click(function () {
        url = 'activity_export?key='+$(".searchVal").val();
        url+='&start_time='+$(".start_time").val();
        url+='&end_time='+$(".end_time").val();
        url+='&is_recmd='+$(".is_recmd").val();
        $('#downloadexcel').attr('src',url);
    })

    //列表操作
    table.on('tool(activityList)', function(obj){
        var layEvent = obj.event,
            data = obj.data;
        if(layEvent === 'edit'){ //编辑
            editActivity(data);
        }else if(layEvent === 'see'){
            activityList(data);
        }else if(layEvent === 'usable'){ //启用禁用
            var _this = $(this),
                usableText = "是否确定禁用此活动？",
                btnText = "已禁用";
            if(_this.text()=="已禁用"){
                usableText = "是否确定启用此活动？",
                    btnText = "已启用";
            }
            layer.confirm(usableText,{
                icon: 3,
                title:'系统提示',
                cancel : function(index){
                    layer.close(index);
                }
            },function(index){
                _this.text(btnText);
                layer.close(index);
            },function(index){
                layer.close(index);
            });
        }else if(layEvent === 'del'){ //删除
            layer.confirm('确定删除此活动？',{icon:3, title:'提示信息'},function(index){
                $.post("activity_delete",{
                    ids : data.id,  //将需要删除的newsId作为参数传入
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                },function(data){
                    tableIns.reload();
                    layer.close(index);
                })
            });
        }
    });
})
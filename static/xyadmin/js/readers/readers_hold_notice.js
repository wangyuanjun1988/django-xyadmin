layui.use(['layer', 'form', 'element'], function(){
  var layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery
  ,form = layui.form
  ,element = layui.element;

  //……

  //但是，如果你的HTML是动态生成的，自动渲染就会失效
  //因此你需要在相应的地方，执行下述方法来进行渲染
    form.render();

    /*监听禁用启用开关*/
	form.on('switch(checkedStatus)', function(obj){
	    data.elem.checked ;
	});

  $(".layui-btn").click(function(){
        $.post("readers_hold_notice",{
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
          status:$('input[name="status"]:checked').val()
        },function(res){
          if (res.code == '1') {
            layer.msg("保存成功！");
          }
        })
    })

});
targetImg = document.getElementById("targetImg")

targetImg.addEventListener("mousewheel", function(event) {
    console.log("wheel action!")
    var delta = Math.max(-1, Math.min(1, (event.wheelDelta || -event.detail)));  
    targetImg.style.width = getComputedStyle(targetImg)["width"] + (30 * delta) + "px";   
    targetImg.style.height = "auto";
    console.log(event.wheelDelta, targetImg.style.width, targetImg.style.height);
});

var mx, my, ox, oy; 						// 定义备用变量
function e(event){ 							// 定义事件对象标准化函数
   if( !event){ 							// 兼容IE浏览器
      event = window.event;
      event.target = event.srcElement;
      event.layerX = event.offsetX;
      event.layerY = event.offsetY;
   }
   event.mx = event.pageX || event.clientX + document.body.scrollLeft; 
	// 计算鼠标指针的x轴距离
   event.my = event.pageY || event.clientY + document.body.scrollTop; 
	// 计算鼠标指针的y轴距离
   return event; 							// 返回标准化的事件对象
}
// 定义鼠标事件处理函数
targetImg.onmousedown = function(event){ 	// 按下鼠标时，初始化处理
   event = e(event); 						// 获取标准事件对象
   o = targetImg; 						// 获取当前拖放的元素
   ox = parseInt(o.offsetLeft); 			// 拖放元素的x轴坐标
   oy = parseInt(o.offsetTop); 				// 拖放元素的y轴坐标
   mx = event.mx; 							// 按下鼠标指针的x轴坐标
   my = event.my; 							// 按下鼠标指针的y轴坐标
   targetImg.onmousemove = move; 			// 注册鼠标移动事件处理函数
   targetImg.onmouseup = stop; 				// 注册松开鼠标事件处理函数
}
function move(event){ 						// 鼠标移动处理函数
   event = e(event);
   o.style.left = ox + event.mx - mx  + "px";	// 定义拖动元素的x轴距离
   o.style.top = oy + event.my - my + "px";	// 定义拖动元素的y轴距离
}
function stop(event){ 							// 松开鼠标处理函数
   event = e(event);
   ox = parseInt(o.offsetLeft); 				// 记录拖放元素的x轴坐标
   oy = parseInt(o.offsetTop); 					// 记录拖放元素的y轴坐标
   mx = event.mx ; 								// 记录鼠标指针的x轴坐标
   my = event.my ; 								// 记录鼠标指针的y轴坐标
   o = document.onmousemove = document.onmouseup = null; 
	// 释放所有操作对象
}


(function($) {
	$.extend(true, window, {

        util : {
            currentWidth : function() {
                return $(window).width();
            },
            currentHeight : function(){
                return $(window).height();
            },
            displayType : function() {
                var currentWidth = $(window).width();
                var currentHeight = $(window).height() - 51;
                var displayType = "";

                if (currentWidth >= 1200)
                    displayType = "S1200";
                else if (currentWidth >= 992 && currentWidth < 1200)
                    displayType = "S1199";
                else if (currentWidth >= 768 && currentWidth < 992)
                    displayType = "S0991";
                else if (currentWidth < 768)
                    displayType = "S0767";

                return displayType;
            },
            BrowserDetect : {
                init : function() {
                    this['browser'] = this.searchString(this.dataBrowser) || "Other";
                    this['version'] = this.searchVersion(navigator.userAgent) || this.searchVersion(navigator.appVersion) || "Unknown";
                },
                searchString : function(data) {
                    for (var i = 0; i < data.length; i++) {
                        var dataString = data[i].string;
                        this.versionSearchString = data[i].subString;

                        if (dataString.indexOf(data[i].subString) !== -1) {
                            return data[i].identity;
                        }
                    }
                },
                searchVersion : function(dataString) {
                    var index = dataString.indexOf(this.versionSearchString);
                    if (index === -1) {
                        return;
                    }

                    var rv = dataString.indexOf("rv:");
                    if (this.versionSearchString === "Trident" && rv !== -1) {
                        return parseFloat(dataString.substring(rv + 3));
                    } else {
                        return parseFloat(dataString.substring(index + this.versionSearchString.length + 1));
                    }
                },
                dataBrowser : [ {
                    string : navigator.userAgent,
                    subString : "Edge",
                    identity : "MS Edge"
                }, {
                    string : navigator.userAgent,
                    subString : "MSIE",
                    identity : "Explorer"
                }, {
                    string : navigator.userAgent,
                    subString : "Trident",
                    identity : "Explorer"
                }, {
                    string : navigator.userAgent,
                    subString : "Firefox",
                    identity : "Firefox"
                }, {
                    string : navigator.userAgent,
                    subString : "Opera",
                    identity : "Opera"
                }, {
                    string : navigator.userAgent,
                    subString : "OPR",
                    identity : "Opera"
                }, {
                    string : navigator.userAgent,
                    subString : "Chrome",
                    identity : "Chrome"
                }, {
                    string : navigator.userAgent,
                    subString : "Safari",
                    identity : "Safari"
                } ]
            },
            msg : {
                init : msgInit,
                alertAutoClose : alertAutoClose,
                alert : alertDialog,
                confirm : confirmDialog,
                focusNavigate : focusNavigateTip,
                confirmOpts : confirmOpts
            },
            isMobile : {
                Android: function() {
                    return navigator.userAgent.match(/Android/i)?true:false;
                },
                BlackBerry: function() {
                    return navigator.userAgent.match(/BlackBerry/i)?true:false;
                },
                iOS: function() {
                    return navigator.userAgent.match(/iPhone|iPad|iPod/i)?true:false;
                },
                Opera: function() {
                    return navigator.userAgent.match(/Opera Mini/i)?true:false;
                },
                Windows: function() {
                    return (navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i))?true:false;
                },
                any: function() {
                    return (this.Android() || this.BlackBerry() || this.iOS() || this.Opera() || this.Windows());
                }
            }				
        }

	});

	util.BrowserDetect.init();

	/*
	 * navigatee focus tooltip param: - id : id or $(id) - msg: 메세지 2013.02.02,
	 * mvp
	 */
	var timeObj;
	var navigate$;
	function focusNavigateTip(id,msg){
		if(timeObj) { 
			clearTimeout(timeObj); timeObj = undefined ;
		};
		var target$; 
		if($.type(id) == 'string') {
			target$ = $("#"+id);
		}else if(id.length > 0){  //$obj로 넘어 왔을 경우
			target$ = id;
		}

		if(target$.parents('.search-condition-parent').length > 0) { 
			target$.parents('.search-condition').css("display","block");
		} 

		if(navigate$) {
			if(target$[0] == navigate$[0]) {
				destroy();
			} else {
				navigate$.removeClass('point-focus').tooltip( "destroy" );	
				setTimeout(goTooltip,100);
			}
		} else {
			setTimeout(goTooltip,100);
		}

		function goTooltip() {
			navigate$ = target$;
			navigate$.attr("title", msg).addClass('point-focus');
			navigate$.tooltip({
				placement : function(context, element){
					var top = $(element).parents('.nicescroll-bar').scrollTop() +  $(element).offset().top;
					if(top < 110) return "bottom";
					
					return "top";
				}
			});
			navigate$.tooltip('show');	
			destroy();
		}
		
		function destroy(){
			var top = navigate$.parents('.nicescroll-bar').scrollTop() +  navigate$.offset().top - 100;
			if(top < 0) top = 0;
			if(navigate$.parents('.slimScrollDiv').length > 0) navigate$.parents('.nicescroll-bar').slimScroll( {scrollTo : top } );
			else navigate$.parents('.nicescroll-bar').animate({scrollTop: navigate$.offset().top	}, 1000);
			
			timeObj = setTimeout(function(){
				navigate$.removeClass('point-focus').tooltip( "destroy" );	
				navigate$ = undefined;
			},4000)		
		}
	}

	function msgInit() {
		if( $('.alert-wrap').length > 0 ) $('.alert-wrap').remove();

		$('body').append(
		'	<div class="alert-wrap">															'+
		'		<div class="confirmWindow-wrap wrap">												'+
		'			<div class="wrap-inner">														'+
		'				<p class="iconImage-wrap">													'+
		'					<i class="far fa-question-circle"></i>										'+
		'				</p>																'+
		'				<p class="Massage-wrap"></p>									'+
		'				<p class="subMassage-wrap"></p>												'+
		'				<div class="btn-wrap">													'+
		'					<button type="submit" name="confirmOkBT" id="confirmOkBT" class="confirm_OkBT"><i>확인</i></button>		'+
		'					<button type="reset" name="confirmCancelBT" id="confirmCancelBT" class="confirm_CancelBT"><i>취소</i></button>	'+
		'				</div>															'+
		'			</div>																'+
		'		</div>																'+
		'		<div class="alertWindow-wrap wrap">												'+
		'			<div class="wrap-inner">													'+
		'				<p class="iconImage-wrap">												'+
		'					<!--i class="fas fa-exclamation-circle"></i-->									'+
		'					<i class="bi bi-x-circle-fill"></i>									'+		
		'				</p>															'+
		'				<p class="Massage-wrap"></p>									'+
		'				<p class="subMassage-wrap"></p>												'+
		'				<div class="btn-wrap">													'+
		'					<button type="button" name="alertCloseBt" id="alertCloseBt"><i>확인</i></button>				'+
		'				</div>															'+
		'			</div>																'+
		'		</div>																'+
		'		<div class="auto-closeW-wrap wrap">												'+
		'			<div class="wrap-inner">													'+
		'				<p class="iconImage-wrap">												'+
		'					<i class="far fa-check-circle"></i>										'+
		'				</p>															'+
		'				<p class="Massage-wrap"></p>								'+
		'				<p class="subMassage-wrap">3초후에 자동으로 닫힙니다.</p>								'+
		'			</div>																'+
		'		</div>																	'+
		'	</div>																		');
			
		$('.alert-wrap button').off('click');
	}

	/* alertAutoClose show
	 * param:
	 *  - message: 메세지
	 *  - okcallback: 확인 선택시 실행 function
	 * 2013.02.02, mvp
	 */
	var autoCloseInterval;
	function alertAutoClose(message){
		loadingBar.stop();
		msgInit();

		if(autoCloseInterval) {clearInterval(autoCloseInterval);	 autoCloseInterval = undefined; }
		$('.alert-wrap .auto-closeW-wrap').show();	
		var newMessage = message.replace('\n','<br>');
		$('.alert-wrap .Massage-wrap').html(newMessage);

		$('.alert-wrap #autoCloseBt').click(function(){
			$('.alert-wrap .auto-closeW-wrap').hide();
		});

		var timer = 2;
		$('.auto-closeW-wrap #autoCloseBt i').text('확인 ('+timer+')');
		autoCloseInterval = setInterval(function(){
			if(timer <= 1) {
				clearInterval(autoCloseInterval);	
				autoCloseInterval = undefined;
				$('.alert-wrap .auto-closeW-wrap').hide();
			}
			timer--;
		}, 1000);
	}

	/* alert Dialog show
	 * param:
	 *  - message: 메세지
	 *  - okcallback: 확인 선택시 실행 function
	 * 2013.02.02, mvp
	 */
	function alertDialog(message, callback){
		msgInit();
		$('.alert-wrap .alertWindow-wrap').show();
		
		var newMessage = message.replace('\n','<br>');
		$('.alert-wrap .Massage-wrap').html(message);

		$('.alert-wrap #alertCloseBt').click(function(){
			$('.alert-wrap .alertWindow-wrap').hide();
			if( $.type(callback) == 'function') callback();
		});
		
		setTimeout(function(){
			$('.alert-wrap #alertCloseBt').focus();	
		},10);		
	}

	/* confirm Dialog show
	 *
	 * param:
	 *  - message: 메세지
	 *  - okcallback: 확인 선택시 실행 function
	 * 2013.02.02, mvp
	 */  
	function confirmDialog(message, okCallback, cancelCallback){
		msgInit();
		$('.alert-wrap .confirmWindow-wrap').show();
		
		var newMessage = message.replace('\n','<br>');
		$('.alert-wrap .Massage-wrap').html(message);

		$('.alert-wrap #confirmOkBT').click(function(){
			$('.alert-wrap .confirmWindow-wrap').hide();
			if( $.type(okCallback) == 'function') okCallback();
		})

		$('.alert-wrap #confirmCancelBT').click(function(){
			$('.alert-wrap .confirmWindow-wrap').hide();
			if( $.type(cancelCallback) == 'function') cancelCallback();
		});
	}

		/* confirm Dialog show
	 *
	 * param:
	 *  - message: 메세지
	 *  - okcallback: 확인 선택시 실행 function
	 * 2013.02.02, mvp
	 */  
	function confirmOpts(opts){
		 var basicOpts = $.extend({
			 message : "",
			 button : [{
				title : '확인',
				style : 'b-middle b-save',			
				callback : function(){}
			 },{
				title : '취소',
				style : 'b-middle b-cancle',		
				callback : function(){}
			 }]
		 },opts);

		msgInit(); var newMessage = basicOpts.message.replace(/\n/gi,'<br>'); 
		$('.alert-wrap .Massage-wrap').html(newMessage);

		$('.confirmWindow-wrap .btn-wrap').html('');

		var buttonHtml = '<button type="reset" class="button"><i>취소</i></button>';		
		$.each(basicOpts.button,function(i,val){
			var buttonHtml$ = $(buttonHtml);
			buttonHtml$.find('i').html(val.title);
			buttonHtml$.addClass(val.style);
			$('.confirmWindow-wrap .btn-wrap').append(buttonHtml$);

			buttonHtml$.on('click',val, function(event){
				$('.alert-wrap .confirmWindow-wrap').hide();
				if( $.type(event.data.callback) == 'function') event.data.callback();
			})
		})
		$('.alert-wrap .confirmWindow-wrap').show();
	}

})(jQuery);
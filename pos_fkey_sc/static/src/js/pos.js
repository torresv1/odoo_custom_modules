openerp.pos_fkey_sc = function(instance){
	instance.point_of_sale.PosWidget = instance.point_of_sale.PosWidget.extend({
		start: function() {
            var self = this;
            return self.pos.ready.done(function() {
                // remove default webclient handlers that induce click delay
                $(document).off();
                $(window).off();
                $('html').off();
                $('body').off();
                $(self.$el).parent().off();
                $('document').off();
                $('.oe_web_client').off();
                $('.openerp_webclient_container').off();
                document.onkeydown = function(e) {
                	if(e.which == 120){
                		if(self.pos.get('selectedOrder') && self.pos.get('selectedOrder').get('orderLines') && self.pos.get('selectedOrder').get('orderLines').length){
	                		if (self.pos.get('selectedOrder').get('screen') === 'receipt'){  //TODO Why ?
	                            console.warn('TODO should not get there...?');
	                            return;
	                        }
	                		var flag = true
	                		_.each(self.pos.cashregisters, function(register){
	                			if (register.journal.type == 'cash' && flag){
	                				self.pos.get('selectedOrder').addPaymentline(register);
	    	                        self.pos_widget.screen_selector.set_current_screen('payment');
	    	                        flag = false
	                			}
	                		})
                		}
                	}else if(e.which == 121){
                		self.payment_screen.validate_order()
                		self.receipt_screen.finishOrder()
                	}
                };
                self.build_currency_template();
                self.renderElement();
                
                self.$('.neworder-button').click(function(){
                    self.pos.add_new_order();
                });

                self.$('.deleteorder-button').click(function(){
                    if( !self.pos.get('selectedOrder').is_empty() ){
                        self.screen_selector.show_popup('confirm',{
                            message: _t('Destroy Current Order ?'),
                            comment: _t('You will lose any data associated with the current order'),
                            confirm: function(){
                                self.pos.delete_current_order();
                            },
                        });
                    }else{
                        self.pos.delete_current_order();
                    }
                });
                
                //when a new order is created, add an order button widget
                self.pos.get('orders').bind('add', function(new_order){
                    var new_order_button = new instance.point_of_sale.OrderButtonWidget(null, {
                        order: new_order,
                        pos: self.pos
                    });
                    new_order_button.appendTo(this.$('.orders'));
                    new_order_button.selectOrder();
                }, self);

                self.pos.add_new_order();

                self.build_widgets();

                if(self.pos.config.iface_big_scrollbars){
                    self.$el.addClass('big-scrollbars');
                }

                self.screen_selector.set_default_screen();

                self.pos.barcode_reader.connect();

                instance.webclient.set_content_full_screen(true);

                self.$('.loader').animate({opacity:0},1500,'swing',function(){self.$('.loader').addClass('oe_hidden');});

                self.pos.push_order();

            }).fail(function(err){   // error when loading models data from the backend
                self.loading_error(err);
            });
        },
	})
}


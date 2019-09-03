--目前已实现功能:
--连接wifi
--控制舵机
--发送请求
pin = 13
wifi.setmode(wifi.STATION)
wifi.sta.config("账号","密码")
wifi.sta.connect()
tmr.alarm(1, 1000, 1, function()
if wifi.sta.getip()== nil then
    print("IP unavaiable, Waiting...")
else
    tmr.stop(1)
    print("Config done, IP is "..wifi.sta.getip())
end
end)
function control_ser_l()
    --控制舵机下拉函数
    pmw.setup(pin, 50, 921)
    pmw.start(pin)
end
function control_ser_e()
    --控制舵机复位函数
    pmw.setup(pin, 50, 947)
    pmw.start(pin)
end
function control_ser_h()
    --控制舵机上拉函数
    pmw.setup(pin, 50 , 972)
    pmw.start(pin)
end
function send_data()
    --发送数据函数
    http.post('http://',
   'Content-Type: application/json\r\n',
   '{"secret_key":"hello"}',
        function(code, data)
            if (code < 0) then
                print("HTTP request failed")
            else 
                return data
            end
            end)
end
tmr.alarm(2,1000,1,function()
    --周期为1秒
    data = send_data()
    if (data==0) then
       control_ser_low() 
       tmr.delay(500)
       control_ser_e()
    elseif(data==1) then
	control_ser_h()
	tmr.delay(500)
	vontrol_ser_e()
    end
end
)

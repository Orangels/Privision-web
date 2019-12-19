import React from 'react';
import io from 'socket.io-client'
import video from 'video.js';
import videoSWF from 'videojs-swf/dist/video-js.swf';
import "video.js/dist/video-js.css";
import back from '../../assets/back/back_large.jpg'

const uri = 'http://localhost/test';
const options = { transports: ['websocket'] };


class App extends React.Component{
    // 构造
    constructor(props) {
        super(props);
        // 初始状态
        this.state = {
            src:back
        };

        this._ws_new_state = this._ws_new_state.bind(this)
        this.socket = 1


    }

    url = 'http://127.0.0.1:9000/set_imgs'
    ws_url = 'http://127.0.0.1:9000/Camera_Web_ws'


    _ws_new_state(data){
        let start = new Date().getTime()

        this.setState({
            src:`data:image/png;base64,${data.data.img}`
            // src:`http://192.168.88.91:9000${data.data.img}`
        },()=>{
            // let end =new Date().getTime()
            // // console.log(`${end} - ${start} = ${end-start}`)
            // console.log(`${end} - ${this.start_time} = ${end-this.start_time}`)
            // this.start_time = end
        })
        let end =new Date().getTime()
        // console.log(`${end} - ${start} = ${end-start}`)
        console.log(`${end} - ${this.start_time} = ${end-this.start_time}`)
        this.start_time = end
    }

    componentDidMount() {

        // let url = window.location.origin;
        let url = '192.168.88.91:9000/'
        url = `${url}Camera_Web_ws`
        // let socket = io(url);

        //本机测试 用固定 url
        console.log('长连接 服务器')
        this.socket = io(url)
        this.socket.on('new_state',this._ws_new_state);
        this.start_time = new Date().getTime()
        // this.socket.on('new_person_state',this._ws_new_person_state);

    }

    componentWillUnmount() {
        this.socket.emit('disconnect')
    }


    render() {
        let content_1_height = 500
        return(
            <div className="Mode_1">
                <img ref={(e)=>this.ref=e} width="100%" height="600" src={this.state.src}/>
            </div>
        )
    }

}



export default App;

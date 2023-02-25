import axios from 'axios';
import mongoose from 'mongoose';
import db from '../../lib/db';
import Tweet from '../../models/tweet';


export default async function handler(req, res) {
    if(req.method === 'POST') {
        mongoose.set('strictQuery', true);
        await db();
        let {tweet} = req.body
        
        axios.post('http://127.0.0.1:5000/model/toxic-content', {text: tweet.tweet}).then((response) => {
            if(response.data.success){
                if(response.data.predicted_val === 0){
                    tweet.toxicity = false;
                    Tweet.create(tweet).then((respo)=>{
                        if(!respo){
                            return res.json({success: false, message: 'something went wrong'})
                        }
                        return res.json({success: true, message: 'Tweet is not toxic'})
                    }).catch((err)=>{
                        return res.json({success: false, message: 'something went wrong', error: err})
                    })
                }
                else{
                    return res.json({success: false, message: 'Tweet is toxic', error: "send warning to user", error_code: 1})
                }
            }
            else{
                return res.json({success: false, message: 'something went wrong', error: response.data.error})
            }
        })
    }
    else{
        return res.status(200).json({ status: 'active', message: 'Intercept AI' })
    }
  }
  
import mongoose from 'mongoose';
import db from '../../lib/db';
import Tweet from '../../models/tweet';

export default async function handler(req, res) {
    if(req.method === 'GET') {
        await db()
        const tweets = await Tweet.find({username: "@ssahibsingh"}).sort({id: -1})
        if(!tweets){
            return res.json({success: false, message: 'something went wrong'})
        }
        else{
            return res.json({success: true, message: 'tweets fetched', tweets: tweets})
        }
    }
}

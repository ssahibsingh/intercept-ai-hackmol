import mongoose from 'mongoose'
const tweetSchema = new mongoose.Schema({
    id: Number,
    name: String,
    username: String,
    tweet: String,
    tweetType: String,
})

export default mongoose.models.Tweet || mongoose.model("Tweet", tweetSchema)
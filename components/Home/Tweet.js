import Image from "next/image";
import React, { useEffect, useState } from "react";

const Tweet = ({ _id, name, username, tweet, tweetType, format }) => {
  const [showImage, setShowImage] = useState(false);
  const [src, setSrc] = useState(null);

  useEffect(() => {
    let blob = new Blob([tweet], { type: `image/${format}` });
    let url = URL.createObjectURL(blob);
    setSrc(url);
  }, [format, tweet]);

  return (
    <>
      <hr className="m-0 p-0" />
      <div className="tweet m-0 py-2 px-2">
        <p className="name">
          {name} · <span className="text-muted">{username}</span>
        </p>
        {tweetType === "text" && <p className="m-0">{tweet}</p>}
        {tweetType === "image" && (
          <Image
            src={`http://127.0.0.1:5000/image/${_id}`}
            alt="tweet"
            className="tweet-image"
            width={100}
            height={100}
          />
        )}
      </div>
      {/* <hr className='m-0 p-0'/> */}
    </>
  );
};

export default Tweet;

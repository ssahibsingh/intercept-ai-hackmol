import axios from "axios";
import Image from "next/image";
import React, { useMemo, useState } from "react";
import { useDropzone } from "react-dropzone";
import { BsFolder } from "react-icons/bs";
// import HashLoader from "react-spinners/HashLoader";

const baseStyle = {
  flex: 1,
  width: "100%",
  height: "15vh",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  //   padding: "20px",
  borderWidth: "5px",
  borderRadius: "30px",
  //   borderColor: "#d2a52a8d",
  borderColor: "#999",
  borderStyle: "dashed",
  // backgroundColor: "#a2c1a593",
  // backgroundColor: "#cdf0d0",
  backgroundColor: "#fff",
  color: "#000",
  outline: "none",
  transition: "border .24s ease-in-out",
};

const focusedStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00B895",
};

const rejectStyle = {
  borderColor: "#8b152d",
};

const Drag = () => {
  const [file, setFile] = useState(null);
  const [errorDrag, setErrorDrag] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showDropZone, setShowDropZone] = useState(true);
  const {
    acceptedFiles,
    fileRejections,
    getRootProps,
    getInputProps,
    isDragActive,
    isFocused,
    isDragAccept,
    isDragReject,
  } = useDropzone({
    accept: { "image/*": [] },
    maxFiles: 1,
    onDrop: (acceptedFiles, fileRejectionItems) => {
      if (fileRejectionItems.length > 0) {
        setErrorDrag(fileRejectionItems[0].errors[0].message);
      }

      if (acceptedFiles.length > 0) {
        setErrorDrag(null);
        setResult(null);
        let cfile = acceptedFiles[0];
        cfile.preview = URL.createObjectURL(cfile);
        // console.log(cfile);
        setFile(cfile);
        setShowDropZone(false);
      }
    },
  });

  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isFocused ? focusedStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {}),
    }),
    [isFocused, isDragAccept, isDragReject]
  );

  const handleUpload = async () => {
    setLoading(true);
    let formData = new FormData();
    formData.append("image", file);
    const config = {
      headers: { "content-type": "multipart/form-data" },
    };
    try {
      setFile(null);
      let response = await axios.post(
        "http://127.0.0.1:5000/model/check-image",
        formData,
        config
      );
      console.log(response.data);
      if (response.data.success) {
        setResult(response.data);
        setFile(null);
        setErrorDrag(null);
      } else {
        setErrorDrag(response.data.message);
        setFile(null);
      }
    } catch (error) {
      console.log(error);
      setErrorDrag(error.message);
    }
    setLoading(false);
  };
  return (
    <>
      <div className="text-center">
          {showDropZone && (
            <div {...getRootProps({ style })}>
              <input {...getInputProps()} />
              <div className={isDragActive ? "text-muted" : null}>
                <div>
                  <BsFolder
                    className={
                      isDragActive ? "drop-icon text-muted" : "drop-icon"
                    }
                  />
                  <p>
                    Upload or Drag and <br></br>drop your image
                  </p>
                </div>
              </div>
            </div>
          )}
        {file && file.preview && (
          <div className="mt-3">
            <div className="container">
              <div className="row text-center justify-content-center">
                <div className="col-md-10 col-12 image-preview">
                  <div className="d-flex justify-content-around align-items-center">
                    <div className="row justify-content-around align-items-center p-2">
                      <div className="col-auto">
                        <Image
                          className="rounded img-fluid"
                          src={file.preview}
                          alt=""
                          width={150}
                          height={150}
                        />
                      </div>
                      <div className="col-auto">
                        <p className="">{file.name}</p>
                      </div>
                    </div>
                    <div className="row justify-content-around align-items-center">
                      <div className="col-auto d-flex ustify-content-around align-items-center gap-1">
                        <button
                          onClick={() => {
                            setFile(null);
                            setShowDropZone(true);
                          }}
                          className="btn-danger p-0 px-2 pb-1 btn rounded-circle "
                        >
                          x
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="mt-1">
          <div className="row text-center justify-content-center">
            {errorDrag ? (
              <>
                <div className="col-12">
                  <p className="text-danger">{errorDrag}</p>
                </div>
              </>
            ) : (
              <></>
            )}
          </div>
        </div>
        {loading && (
          <div className="mt-3">
            {/* <HashLoader className="mx-auto" color="#6aba5e" /> */}
            <p>Posting.... Please Wait</p>
          </div>
        )}
        {result && (
          <div className="mt-3">
            <div className="row justify-content-center align-items-center ">
              <div className="col-md-6 col-sm-12 col-12 mb-2">
                <Image
                  className="rounded img-fluid"
                  src={`http://127.0.0.1:5000/image/${result.image_id}`}
                  alt=""
                  width={150}
                  height={150}
                />
              </div>
              <div className="col-md-6 col-sm-12 col-12 text-second text-center mt-2">
                <p>
                  Prediction:{" "}
                  <span className="text-capitalize fw-bold">
                    {result.prediction}
                  </span>
                </p>
                <p>
                  Confidence:{" "}
                  <span className="fw-bold">{result.confidence}</span>
                </p>
              </div>
            </div>
          </div>
        )}
        <div className="text-end">
          <button
            className={
              file
                ? "btn btn-dark rounded-pill"
                : "btn btn-dark rounded-pill disabled"
            }
            onClick={handleUpload}
          >
            Post
          </button>
        </div>
      </div>
    </>
  );
};

export default Drag;

import { Navbar } from "@/components";
import axios from "axios";
import { Field, Form, Formik } from "formik";
import Head from "next/head";
import React, { useState } from "react";
import { FiSend } from "react-icons/fi";

const Youtube = () => {
  const [error, setError] = useState(true);
  const [messages, setMessages] = useState([
    {
      id: 1,
      message: "Hello",
    },
    {
      id: 2,
      message: "Hello",
    },
    {
      id: 3,
      message:
        "Hello lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quod.",
    },
  ]);

  const initialValues = {
    message: "",
  };

  const validate = (values) => {
    const errors = {};
    if (!values.message) {
      errors.message = "Required";
    }

    if (Object.keys(errors).length !== 0) {
      setError(true);
    } else {
      setError(false);
    }
    return errors;
  };

  const onSubmit = (values, onSubmitProps) => {
    onSubmitProps.setSubmitting(true);

    axios.post("http://127.0.0.1:5000/model/similarity", { text: values.message }).then((response) => {
      if (response.data.success) {
        console.log(response.data.prediction);
        if (response.data.prediction === "0") {
          setMessages(() => [
            ...messages,
            { id: messages.length + 1, message: values.message },
          ]);
        }else{
            // alert("Blocked Words Detected")
        }
      }
    });
    onSubmitProps.resetForm();
  };
  return (
    <>
      <Head>
        <title>YouTube UseCase</title>
      </Head>
      <div className="">
        <Navbar />
        <div className="container-fluid my-4">
          <div className="row justify-content-center">
            <div className="col-md-8 col-12">
              <iframe
                className="rounded"
                width="100%"
                height="576"
                src="https://www.youtube.com/embed/QlHVD7x7gvE?list=RDkzuYlTTvVFA&autoplay=0&loop=1&mute=1"
                title="Secret (Official Video) Zehr Vibe | Addiction | Jatt Life Studios | Sky | Latest Punjabi Songs 2023"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              ></iframe>
            </div>
            <div className="col-md-3 col-6 border rounded">
              <div className="d-flex align-items-end h-100">
                <div className="w-100">
                  <ul className="list-unstyled py-2">
                    {messages &&
                      messages.map((item) => {
                        return (
                          <li key={item.id} className="border-top px-3 my-2">
                            {item.message}
                          </li>
                        );
                      })}
                  </ul>
                  <div className="mb-3">
                    <Formik
                      onSubmit={onSubmit}
                      initialValues={initialValues}
                      validate={validate}
                    >
                      <Form className="d-flex justify-content-around">
                        <Field
                          type="text"
                          name="message"
                          className="form-control w-75"
                          id="message"
                          aria-describedby="emailHelp"
                          placeholder="Enter Message"
                        />
                        <button type="submit" className="btn btn-dark">
                          Send
                        </button>
                      </Form>
                    </Formik>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Youtube;

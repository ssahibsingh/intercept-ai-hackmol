import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import styles from "@/styles/Home.module.css";
import { Main, Sidebar } from "@/components";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <Head>
        <title>Intercept AI</title>
      </Head>
      <div className="container">
        <div className="row">
          <div className="col-md-3 col-sm-2">
            <Sidebar/>
          </div>
          <div className="col-md-5 col-sm-10 border m-0 p-0">
            <Main />
          </div>
        </div>
      </div>
    </>
  );
}

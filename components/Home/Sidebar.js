import React from "react";
import { RiHome7Fill } from "react-icons/ri";
import {GiFeatherWound} from "react-icons/gi";
import {GrNotification} from "react-icons/gr";
import {BiUser} from "react-icons/bi";
import {BsBookmark} from "react-icons/bs";
import {FaHashtag} from "react-icons/fa";
import {FiMail} from "react-icons/fi";
import {CgMoreO} from "react-icons/cg";

const Sidebar = () => {
    const sidebar = [
        {
            id: 1,
            icon: <RiHome7Fill className="mx-3" />,
            name: "Home"
        },
        {
            id: 2,
            icon: <FaHashtag className="mx-3" />,
            name: "Explore"
        },
        {
            id: 3,
            icon: <GrNotification className="mx-3"/>,
            name: "Notification"
        },
        {
            id: 4,
            icon: <FiMail className="mx-3" />,
            name: "Messages"
        },
        {
            id: 5,
            icon: <BsBookmark className="mx-3" />,
            name: "Bookmarks"
        },
        {
            id: 6,
            icon: <BiUser className="mx-3"/>,
            name: "Profile"
        },
        {
            id: 7,
            icon: <CgMoreO className="mx-3"/>,
            name: "More"
        }
    ]
  return (
    <>
      <div className="min-vh-100">
        <div className="d-flex flex-column justify-content-between sidebar">
          <div className="links pt-5">
            <div className="logo text-primary text-center"><h2>Twitter</h2></div>
            <ul className="list-unstyled">
            {sidebar && sidebar.map((item)=>{
                return(
                    <li key={item.id} className="my-4 fs-5 sidebar-links">
                    {item.icon}
                    {item.name}
                  </li>
                )
            })}
            </ul>
          </div>
          <div className="sidebar-profile mb-4 px-3">
            <p className="m-0">SAHIB SINGH</p>
            <span className="text-muted">@ssahibsingh</span>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;

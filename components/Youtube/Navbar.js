import React from 'react'
import { HiMenu } from 'react-icons/hi'
import {BsSearch} from 'react-icons/bs'
const Navbar = () => {
    return (
        <>
            <nav className="navbar navbar-expand-lg bg-body-tertiary">
                <div className="container-fluid">
                    <HiMenu className="fs-3 mx-2" />
                    <p className="navbar-brand text-danger fs-3 m-0 p-0">
                        Youtube
                    </p>
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <div className="mx-auto">
                            <form className="d-flex" role="search">
                                <input
                                    className="form-control me-2 rounded-pill col-md-6"
                                    type="search"
                                    placeholder="Search"
                                    aria-label="Search"
                                />
                                <button
                                    className="btn btn-outline-secondary rounded-pill"
                                    type="submit"
                                >
                                    <BsSearch/>
                                </button>
                            </form>
                        </div>
                    </div>
                    <div className="mx-5"></div>
                </div>
            </nav>
        </>
    )
}

export default Navbar
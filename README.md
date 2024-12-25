# Agentic Leave App

Employee Leave Application using Autogen Agentic AI 

### Overview

Idea is to build an application where agents control the business logic of the application layer,
while the CRUD operations are supported by REST APIs. And there is no UI, but only the chat interface.

This is inspired by Satya Nadella's speech https://www.youtube.com/watch?v=uGOLYz2pgr8

### Architecture

* docker to containerize the app
* mongodb
* python eve for schema and rest api
* autogen with openai for auth and business logic

Roles
* admin - can manage users
* user - can apply leave. has a manager assigned.
* manager - can approve/reject leaves as well as everything a user can do.








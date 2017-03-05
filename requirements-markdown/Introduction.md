# Introduction
Camelot is JSON-based server written exclusively in [Python 3](https://www.python.org/about/). The purpose of Camelot is to provide IRC-esque chatroom functionality.

## Purpose
This document is intended to guide development of Camelot. Not only will it provide the requirements (i.e. system requirements, user requirements, and interface requirements), but it will provide a decent outline for what the server entails (i.e. functions, constraints, dependencies, etc.). Understanding the system requirements will give a more clear and concise understanding of the APIs and their purpose.

## How to Use This Document
Because this document will be reviewed by various different skill sets, this section will break down which parts should be reviewed by which type of reader.

### Types of Reader
### Technical Background Required
Programming competency *is imperative* to understanding the documentation. Programming methodology, jargon, and general concepts will be assumed in subsequent sections.

Server side programming is recommended, but not required. The document will stay to a high level server design.

For the purpose of this document, source code will not appear. Specific tools/programming languages capability is not required.

### Overview Sections
To get a a general understanding of the document, this following sections and subsections should be (chronologically) read:

1. User Characteristics (**SECTION**)
2. Assumptions and Dependencies (**SECTION**)
3. Specific Requirements (**SECTION**)

### Reader-Specific Sections
Types of readers are described as follows.

- Server-side Developers: This would entail anyone interested in working on this particularly instance of the server. All of this document should be read.
- Client-side Developers: This would entail all who would want to get involved in creating a client. The following sections should be read:
    1. Description (**SECTION**)
    2. Specific Requirements (**SECTION**)
- End Users: This would entail anyone that is generally interested, but has no intentions of truly using it standalone.
    1. Product Perspective (**SECTION**)
    2. Product Functions (**SECTION**)
    3. User Characteristics (**SECTION**)

## Scope of the Product
Truthfully, the intention of this project is to get an A in software engineerings. But I actually have to put something here, so.

There is an expectation at the end of the development lifecycle to open source this server. After open sourcing, the server team hopes that Camelot will serve as a model for server-side programming. Because the JSON-based framework would be familiar to people, the team hopes for a some market adoption. Overall, this would be a good model for how a simple server would be maintained.

## Business Case for the Product
There is a real pandemic: there are not enough chat applications. Sure, there's [Messenger](https://www.messenger.com), [Slack](https://slack.com/), [Skype](https://www.skype.com/en/), [Viber](https://www.viber.com/en/), [WeChat](https://web.wechat.com), [WhatsApp](https://www.whatsapp.com), [Line](https://line.me/en/), [GroupMe](https://web.groupme.com), [Snapchat](https://www.snapchat.com), [Voxer](http://voxer.com), but their garbage. The market needs a great server to tackle on these giants, and Camelot will do that.

## Overview of the Requirements Document

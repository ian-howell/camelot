-- test data for the database

-- Commented out portions because the raspberry pi's version of postgresql doesn't support the commands.
INSERT INTO "CHANNEL" VALUES ('Server Team', NULL); --ON CONFLICT (CHANNELID) DO NOTHING;
INSERT INTO "CHANNEL" VALUES ('Client Team', NULL); --ON CONFLICT (CHANNELID) DO NOTHING;
INSERT INTO "CHANNEL" VALUES ('Software Eng. Group', NULL); --ON CONFLICT (CHANNELID) DO NOTHING;

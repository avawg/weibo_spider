CREATE TABLE IF NOT EXISTS `user`(
    `id` BIGINT(10) UNSIGNED PRIMARY KEY,
    `screen_name` VARCHAR(20),
    `gender` VARCHAR(1),
    `description` VARCHAR(200),
    `verified_reason` VARCHAR(200),
    `statuses_count` VARCHAR(20),
    `follow_count` VARCHAR(20),
    `followers_count` VARCHAR(20),
    `fans` JSON,
    `follows` JSON
);
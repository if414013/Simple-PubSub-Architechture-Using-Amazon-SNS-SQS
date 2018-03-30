###############################################################################
#                                  Variables                                  #
###############################################################################
variable "aws-config" {
  type = "map"

  default = {
    region     = "ap-southeast-1"
    access_key = "CHANGE_ME"
    secret_key = "CHANGE_ME"
  }
}

variable "sqs-config" {
  type = "map"

  default = {
    delay_seconds              = 1     #delay time before message become available after send to queue
    visibility_timeout_seconds = 5     #delay time before message become available again to consumer if consumer fail or not delete message from queue
    max_message_size           = 2048  #maximum size of message
    message_retention_seconds  = 86400 #how long message will be stored in a queue after being sended
    receive_wait_time_seconds  = 15    #wait time for consumer to ack message
  }
}

###############################################################################
#                             Cloud Provider Setup                            #
###############################################################################
provider "aws" {
  region     = "${var.aws-config["region"]}"
  access_key = "${var.aws-config["access_key"]}"
  secret_key = "${var.aws-config["secret_key"]}"
}

###############################################################################
#                                   AWS SQS                                   #
###############################################################################
resource "aws_sqs_queue" "pubsub_dead_letter_queue" {
  name                       = "pubsub_dead_letter_queue"
  delay_seconds              = "${var.sqs-config["delay_seconds"]}"
  visibility_timeout_seconds = "${var.sqs-config["visibility_timeout_seconds"]}"
  max_message_size           = "${var.sqs-config["max_message_size"]}"
  message_retention_seconds  = "${var.sqs-config["message_retention_seconds"]}"
  receive_wait_time_seconds  = "${var.sqs-config["receive_wait_time_seconds"]}"
}

resource "aws_sqs_queue" "pubsub_main_queue" {
  name                       = "pubsub_main_queue"
  delay_seconds              = "${var.sqs-config["delay_seconds"]}"
  visibility_timeout_seconds = "${var.sqs-config["visibility_timeout_seconds"]}"
  max_message_size           = "${var.sqs-config["max_message_size"]}"
  message_retention_seconds  = "${var.sqs-config["message_retention_seconds"]}"
  receive_wait_time_seconds  = "${var.sqs-config["receive_wait_time_seconds"]}"
  redrive_policy             = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.pubsub_dead_letter_queue.arn}\",\"maxReceiveCount\":3}"
}

resource "aws_sqs_queue_policy" "sqs_send_policy" {
  queue_url = "${aws_sqs_queue.pubsub_main_queue.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy-pubsub",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.pubsub_main_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.pubsub-sns.arn}"
        }
      }
    }
  ]
}
POLICY
}

###############################################################################
#                     AWS SNS Topic and SNS Subscription                      #
###############################################################################
resource "aws_sns_topic" "pubsub-sns" {
  name = "pubsub-sns"
}

resource "aws_sns_topic_subscription" "pubsub_sqs_target" {
  topic_arn = "${aws_sns_topic.pubsub-sns.arn}"
  protocol  = "sqs"
  endpoint  = "${aws_sqs_queue.pubsub_main_queue.arn}"
}

###############################################################################
#                                    Output                                   #
###############################################################################
output "sns_topic_arn" {
  value = "${aws_sns_topic.pubsub-sns.arn}"
}

output "main_queue_url" {
  value = "${aws_sqs_queue.pubsub_main_queue.id}"
}

output "dead_letter_queue_url" {
  value = "${aws_sqs_queue.pubsub_dead_letter_queue.id}"
}

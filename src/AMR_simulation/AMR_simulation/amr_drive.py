import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher')

        # '/cmd_vel' 주제로 퍼블리셔 생성
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # 주기적으로 명령을 보내기 위한 타이머 생성
        timer_period = 0.1  # 0.1초(10Hz)
        self.timer = self.create_timer(timer_period, self.publish_cmd_vel)

        # 초기 속도 설정
        self.linear_speed = 0.0  # 전진/후진 속도 (m/s)
        self.angular_speed = 0.0  # 회전 속도 (rad/s)

        self.get_logger().info('CmdVelPublisher node started!')

    def publish_cmd_vel(self):
        # Twist 메시지 생성
        msg = Twist()
        msg.linear.x = self.linear_speed  # x 방향 선형 속도 (m/s)
        msg.linear.y = 0.0               # y 방향 선형 속도 (m/s) - 메카넘에서는 사용 가능
        msg.linear.z = 0.0               # z 방향 선형 속도 (m/s)

        msg.angular.x = 0.0              # x 방향 회전 속도 (rad/s)
        msg.angular.y = 0.0              # y 방향 회전 속도 (rad/s)
        msg.angular.z = self.angular_speed  # z 방향 회전 속도 (rad/s)

        # 메시지를 퍼블리시
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing cmd_vel: linear={msg.linear.x}, angular={msg.angular.z}')

    def set_velocity(self, linear, angular):
        # 속도를 업데이트
        self.linear_speed = linear
        self.angular_speed = angular
        self.get_logger().info(f'Updated velocities: linear={linear}, angular={angular}')

def main(args=None):
    rclpy.init(args=args)  # ROS 2 초기화
    cmd_vel_publisher = CmdVelPublisher()

    try:
        # 속도 설정: 1.0 m/s로 전진, 0.5 rad/s로 회전
        cmd_vel_publisher.set_velocity(1.0, 0.5)

        # 노드 실행
        rclpy.spin(cmd_vel_publisher)
    except KeyboardInterrupt:
        cmd_vel_publisher.get_logger().info('Node stopped by user.')
    finally:
        # 노드 종료
        cmd_vel_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

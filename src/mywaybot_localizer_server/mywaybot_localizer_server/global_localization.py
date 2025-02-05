import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
from rcl_interfaces.srv import SetParameters
from geometry_msgs.msg import PoseWithCovarianceStamped
from time import sleep

class GlobalLocalization(Node):
    def __init__(self):
        super().__init__('global_localization_node')
        # create client
        self.relocalization_client = self.create_client(Empty, 'reinitialize_global_localization')
        self.param_client = self.create_client(SetParameters, '/amcl/set_parameters')
        self.amcl_covariance = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.listener_callback, 1)

        # wait for service
        while not self.relocalization_client.wait_for_service(timeout_sec=1.0) \
                and not self.param_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        # covariance를 저장할 변수와 파라미터 재설정 여부 플래그
        self.covariance = None
        self.parameters_reset = False

    def set_amcl_params(self, max_particles, min_particles, is_start):
        params = [
            Parameter(name='max_particles', value=ParameterValue(type=ParameterType.PARAMETER_INTEGER, integer_value=max_particles)),
            Parameter(name='min_particles', value=ParameterValue(type=ParameterType.PARAMETER_INTEGER, integer_value=min_particles))
        ]
        req = SetParameters.Request()

        # print current max_particles and min_particles
        self.get_logger().info('max_particles: %d' % max_particles)
        self.get_logger().info('min_particles: %d' % min_particles)

        if is_start:
            for param in params:
                req.parameters.append(param)

            future = self.param_client.call_async(req)
            future.add_done_callback(self.set_amcl_params_callback)
            return future.result()

    def call_reinitialize_global_localization(self):
        req = Empty.Request()
        return self.relocalization_client.call_async(req)

    def set_amcl_params_callback(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error('Service call failed %r' % (e,))
        else:
            self.get_logger().info('Service call succeeded %r' % (response,))
            self.get_logger().debug(self.covariance)

    def listener_callback(self, msg):
        # covariance 값 업데이트
        self.covariance = msg.pose.covariance
        self.get_logger().info('Received covariance[0]: %f , covariance[7]: %f' % (self.covariance[0], self.covariance[7]))

        # covariance[0]과 covariance[7] 값이 모두 0.006 미만이면 기본 파라미터로 재설정
        if not self.parameters_reset and self.covariance[0] < 0.006 and self.covariance[7] < 0.006:
            self.get_logger().info("Covariance below threshold; resetting AMCL parameters to default.")
            self.set_amcl_params(2000, 500, False)
            self.parameters_reset = True  # 반복 호출 방지

def main(args=None):
    rclpy.init(args=args)
    global_localization = GlobalLocalization()

    # adjust parameters for global localization
    global_localization.set_amcl_params(40000, 500, True)
    rclpy.spin_once(global_localization)

    # call service reinitialize_global_localization
    future = global_localization.call_reinitialize_global_localization()
    rclpy.spin_until_future_complete(global_localization, future)
    if future.result() is not None:
        global_localization.get_logger().info('Global localization reinitialized successfully.')
    else:
        global_localization.get_logger().error('Failed to call service reinitialize_global_localization')

    # restore default parameters
    sleep(10)

    rclpy.spin(global_localization)
    global_localization.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

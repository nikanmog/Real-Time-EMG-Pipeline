import helpers.environment_variables as env
from helpers.communication import receive_signal, send_signal, get_emg_client
from helpers.prediction import get_prediction
from helpers.visualization import plot_force


def main():
    client = get_emg_client(tcp_port=env.TCP_PORT, hostname=env.HOSTNAME)
    try:
        send_signal(client, env.START_SIGNAL)
        while True:
            data = receive_signal(client, env.CHANNELS * env.SAMPLE_RATE * env.CHUNK_SIZE * 2)
            print(data)  # data = np.random.rand(128)
            prediction = get_prediction(data)
            plot_force(prediction)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e, env.ERROR_TEXT)
    finally:
        print(env.STREAM_TEXT)
        send_signal(client, env.STOP_SIGNAL)
        client.close()


if __name__ == '__main__':
    main()

import helpers.communication as comm
import helpers.data_storage as storage
import helpers.environment_variables as env

if __name__ == '__main__':
    print(env.INFO_TEXT)
    client = comm.emg_client(tcp_port=env.TCP_PORT, hostname=env.HOSTNAME)  # Create TCP I/O socket

    try:
        comm.send_signal(client, env.START_SIGNAL)  # Send configuration
        print(env.STREAM_START_TEXT)
        print(env.CHANNELS, env.SAMPLE_RATE, env.CHUNK_SIZE, env.CHANNELS * env.SAMPLE_RATE * env.CHUNK_SIZE)

        while True:
            data = comm.receive_signal(client, env.CHANNELS * env.SAMPLE_RATE * env.CHUNK_SIZE * 2)
            storage.add_recording(data)
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        print(e, env.ERROR_TEXT)
    finally:
        print(env.STREAM_CLOSE_TEXT)
        comm.send_signal(client, env.STOP_SIGNAL)
        client.close()
        storage.persist_recordings()

import click
import icmplib
import ipaddress
import socket


@click.command()
@click.argument('target', type=str, required=True)
@click.option('--lower', type=click.IntRange(0, 1_000_000_000), default=0, help='The lower limit of the search')
@click.option('--upper', type=click.IntRange(0, 1_000_000_000), default=1500, help='The upper limit of the search')
@click.option('--verbose', '-v', is_flag=True, help='Display detailed information')
@click.option('--count', '-c', type=click.IntRange(0, 100), default=3, help='The count of pings per test')
@click.option('--interval', '-i', type=click.FloatRange(0, 5), default=0.1,
              help='The interval between pings within a test')
@click.option('--timeout', '-W', type=click.FloatRange(0, 5), default=1, help='Ping timeout')
def main(target, lower, upper, verbose, count, interval, timeout):
    try:
        ip = ipaddress.ip_address(target)
        print(f'{target} appear to be an IPv{ip.version} address')
    except ValueError:
        print(f'{target} does not appear to be an IPv4 or IPv6 address')
        try:
            _ = socket.gethostbyname(target)
            print(f'{target} appear to be known hostname')
        except socket.gaierror:
            print(f'{target} does not appear to be known hostname')
    except:
        pass
    print('Although it does not matter')

    left = lower - 1
    right = upper + 1
    while left + 1 < right:
        mid = (left + right) // 2
        try:
            ping_res = icmplib.ping(
                target,
                count=count,
                interval=interval,
                timeout=timeout,
                payload_size=mid,
            )
        except icmplib.exceptions.NameLookupError:
            print(f'Host {target} cannot be resolved')
            exit(0)
        except icmplib.exceptions.DestinationUnreachable:
            print(f'Host {target} is unreachable')
            exit(0)
        except:
            print('Unknown icmplib.ping error')
            exit(1)
        if verbose:
            print(f'Sending {mid} bytes: sent={ping_res.packets_sent} '
                  f'received={ping_res.packets_received} '
                  f'loss={ping_res.packet_loss}')
        if ping_res.is_alive:
            left = mid
        else:
            right = mid

    if left == lower - 1:
        print(f'Host {target} is unreachable')
    else:
        print(f'Maximum transmission unit is {left} bytes')


if __name__ == '__main__':
    main()

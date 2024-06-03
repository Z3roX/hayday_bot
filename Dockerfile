FROM openjdk:8

# Install required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    lib32stdc++6 \
    lib32z1 \
    libqt5widgets5 \
    libqt5opengl5 \
    libqt5printsupport5 \
    libqt5gui5 \
    libqt5core5a \
    libqt5network5 \
    libqt5dbus5 \
    libqt5xml5 \
    libqt5sql5 \
    libqt5test5 \
    libqt5concurrent5 \
    libqt5webkit5 \
    libqt5x11extras5 \
    libegl1-mesa \
    libegl1-mesa-dev \
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    libgl1-mesa-dri \
    libgles2-mesa \
    libgles2-mesa-dev \
    libglapi-mesa \
    qemu-kvm \
    libvirt-bin \
    ubuntu-vm-builder \
    bridge-utils \
    mesa-utils \
    x11vnc \
    xvfb \
    supervisor \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN wget https://github.com/novnc/noVNC/archive/refs/tags/v1.2.0.tar.gz -O /tmp/noVNC.tar.gz && \
    tar xzf /tmp/noVNC.tar.gz -C /opt && \
    mv /opt/noVNC-1.2.0 /opt/noVNC && \
    rm /tmp/noVNC.tar.gz

# Install websockify
RUN pip3 install websockify

# Download and unzip Android SDK
RUN mkdir -p /opt/android-sdk-linux
RUN wget -q https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip -O /tmp/tools.zip
RUN unzip /tmp/tools.zip -d /opt/android-sdk-linux
RUN rm /tmp/tools.zip

# Set environment variables
ENV ANDROID_HOME /opt/android-sdk-linux
ENV PATH ${ANDROID_HOME}/tools:${ANDROID_HOME}/tools/bin:${ANDROID_HOME}/platform-tools:${PATH}

# Accept licenses
RUN yes | sdkmanager --licenses

# Install Android emulator
RUN sdkmanager "platform-tools" "platforms;android-29" "emulator"

# Create an AVD (Android Virtual Device)
RUN echo "no" | avdmanager create avd -n test -k "system-images;android-29;default;x86"

# Expose necessary ports
EXPOSE 5554 5555 5900 6080

# Add supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start supervisord
CMD ["/usr/bin/supervisord"]